#!/usr/bin/python
# -*- coding: cp1250 -*-


from urllib.request import urlopen
import re
import requests
import random


polish_letter_conversion = {
    'ÂŚ': 'Ś',
    'Âś': 'ś',
    'ĂŞ': 'ę',
    'Âą': 'ą',
    'ÂŁ': 'Ł',
    'Âł': 'ł',
    'Ăł': 'ó',
    'Ăą': 'ń',
    'ĂŚ': 'ć',
    'Âż': 'ż',
    'ÂŻ': 'Ż',
    'Âź': 'ź',
    'ÂŹ': 'Ź'
}

polish_letter_to_link = {
    'ć': 'cc',
    'ł': 'll',
    'ś': 'ss',
    'ź': 'zz',
    'ż': 'zzz'
}


def all_cities():

    base_url = "http://cybermoon.pl/wiedza/wspolrzedne/wspolrzedne_polskich_miejscowosci_a.html"
    user_agents_list = [
        'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    ]

    r = requests.get(base_url, headers={'User-Agent': random.choice(user_agents_list)})
    find_urls = re.findall(r'<A HREF="wspolrzedne_polskich_miejscowosci_.*?\.html"><B><FONT face="arial" COLOR=".*?" size=".*?">.*?</FONT></B></A>&nbsp;', r.text.encode('utf-8').decode('iso-8859-2'))
    urls = []
    for url in find_urls:
        end_index = url.find('"><B><FONT face=')
        urls.append("http://cybermoon.pl/wiedza/wspolrzedne/" + url[9:end_index])

    found_cities = []

    for url in urls:
        r = requests.get(url, headers={'User-Agent': random.choice(user_agents_list)})
        cities = re.findall(r'<tr><td><font face="Arial" COLOR=c0c0c0 size=2><b>.*?&deg;E</td></tr>', r.text.encode('utf-8').decode('iso-8859-2'))
        found_cities = found_cities + cities

    city_data = dict()

    for city in found_cities:
        new_city = city
        for pattern in polish_letter_conversion.keys():
            new_city = re.sub(pattern, polish_letter_conversion[pattern], new_city)
        name_stop = '</td><td><font face="Arial" COLOR=404040 size=2><b>'
        name_stop_index = new_city.find(name_stop)
        name = new_city[len(name_stop)-1:name_stop_index]
        state_stop = '</td><td><font face="Arial" COLOR=505050 size=2><b>'
        state_stop_index = new_city.find(state_stop)
        state = new_city[name_stop_index+len(name_stop):state_stop_index]
        lon_stop = ' &deg;N&nbsp;&nbsp;</td><td><font face="Arial" COLOR=505050 size=2><b>'
        lon_stop_index = new_city.find(lon_stop)
        lon = new_city[state_stop_index+len(state_stop):lon_stop_index]
        lat_stop = ' &deg;E</td></tr>'
        lat = new_city[lon_stop_index+len(lon_stop):len(lat_stop)*(-1)]

        if name not in city_data.keys():
            city_data[name] = [(state, lon, lat)]
        else:
            prev = city_data[name]
            prev.append((state, lon, lat))
            city_data[name] = prev
        f = open('cities.txt', 'a')
        line = name + ';\t' + state + ';\t' + lon + ';\t' + lat + '\n'
        if line.startswith('Ă'):
            line = "Ć" + name[2:] + ';\t' + state + ';\t' + lon + ';\t' + lat + '\n'
        elif name.startswith('Dz') and name.endswith('erźęcin'):
            line = "Dzierżęcin" + ';\t' + state + ';\t' + lon + ';\t' + lat + '\n'
        elif 'Ă' in name or 'Â' in name:
            line = " "
        print(line)
        f.write(line)
        f.close()


all_cities()
