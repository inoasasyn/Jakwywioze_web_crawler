#!/usr/bin/python
# -*- coding: cp1250 -*-


import re
import psycopg2
import requests
import random
from bs4 import *
import pandas as pd
import os


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
        path = os.getcwd() + "/txt Files/cities.txt"
        f = open(path, 'a')
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


def insert_all_cities():
    path = os.getcwd() + "/txt Files/biggest_cities.txt"
    f = open(path, 'r')
    index = 1
    city = []

    for line in f:
        new_line = line.split(";\t")
        new_line[-1] = new_line[-1][:-1]
        order = [2, 4, 3, 0, 1]
        point = [index] + [new_line[i] for i in order]
        if point[2] != "":
            city.append(tuple(point))
        index += 1

    sql_city = "INSERT INTO city (id, county, latitude, longitude, name, voivodeship) VALUES (%s, %s, %s, %s, %s, %s)"

    conn = None
    try:
        conn = psycopg2.connect(
            dbname='jakwywioze', user='jakwywioze', password='jakwywioze', host='localhost', port='5432'
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.executemany(sql_city, city)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def biggest_cities():
    path = os.getcwd() + "/txt Files/cities.txt"
    f = open(path, 'r')
    prev_cities = dict()

    for line in f:
        new_line = line.split(";\t")
        new_line[-1] = new_line[-1][:-1]
        if new_line[0] not in prev_cities.keys():
            voivodeship_dict = dict()
            voivodeship_dict[new_line[1].lower()] = [[new_line[2], new_line[3]]]
            prev_cities[new_line[0]] = voivodeship_dict
        else:
            current_voivodeship = prev_cities[new_line[0]]
            if new_line[1] not in current_voivodeship.keys():
                current_voivodeship[new_line[1].lower()] = [[new_line[2], new_line[3]]]
            else:
                temp = current_voivodeship[new_line[1]]
                temp.append([new_line[2], new_line[3]])
                current_voivodeship[new_line[1].lower()] = temp

    wikiurl = "https://pl.wikipedia.org/wiki/Lista_powiatów_w_Polsce"
    table_class = "wikitable sortable jquery-tablesorter"
    response = requests.get(wikiurl)
    soup = BeautifulSoup(response.text, 'html.parser')
    indiatable = soup.find('table', {'class': "wikitable"})
    df = pd.read_html(str(indiatable))
    df = pd.DataFrame(df[0])
    col_mapper = dict()
    index = 0
    for x in df.keys():
        col_mapper[x] = index
        index += 1
    df = df.rename(columns=col_mapper)
    powiat = df[0].tolist()
    miasto = df[1].tolist()
    woj = df[3].tolist()

    biggest_cities_dict = dict()
    err_counter = 0
    for i in range(len(df)):
        if miasto[i] != "miasto na prawach powiatu" and miasto[i] not in biggest_cities_dict.keys():
            if miasto[i] in prev_cities.keys():
                found = prev_cities[miasto[i]]
                if woj[i] in found.keys():
                    biggest_cities_dict[miasto[i]] = [woj[i], powiat[i], found[woj[i]][0]]
                else:
                    if len(found.keys()) == 1:
                        for x in found.keys():
                            biggest_cities_dict[miasto[i]] = [woj[i], powiat[i], found[x][0]]
                    else:
                        print('error')
                        err_counter += 1
                        print(miasto[i], end="\t")
                        print(found)
            else:
                print('error')
                err_counter += 1
                print(miasto[i])
        elif powiat[i] == "miasto na prawach powiatu" and powiat[i] not in biggest_cities_dict.keys():
            if powiat[i] in prev_cities.keys():
                found = prev_cities[powiat[i]]
                if woj[i] in found.keys():
                    biggest_cities_dict[powiat[i]] = [woj[i], powiat[i], found[woj[i]][0]]
                else:
                    if len(found.keys()) == 1:
                        for x in found.keys():
                            biggest_cities_dict[powiat[i]] = [woj[i], powiat[i], found[x][0]]
                    else:
                        print('error')
                        err_counter += 1
                        print(powiat[i], end="\t")
                        print(found)
            else:
                print('error')
                err_counter += 1
                print(powiat[i])
    print(err_counter)

    path = os.getcwd() + "/txt Files/biggest_cities.txt"
    f = open(path, 'a')
    for x in biggest_cities_dict.keys():
        line = x + ';\t' + biggest_cities_dict[x][0] + ';\t' + biggest_cities_dict[x][1] + ';\t' + biggest_cities_dict[x][2][0] + ';\t' + biggest_cities_dict[x][2][1] + '\n'
        f.write(line)
    f.close()


#insertuje same miasta
#na razie tylko te bez errorów
#insert_all_cities()


#biggest_cities()
