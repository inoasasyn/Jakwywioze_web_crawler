#!/usr/bin/python
# -*- coding: cp1250 -*-


import re
import requests
import random
from bs4 import *
import pandas as pd
import os


def xd():

    base_url = "http://cybermoon.pl/wiedza/wspolrzedne/wspolrzedne_polskich_miejscowosci_a.html"
    user_agents_list = [
        'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    ]

    r = requests.get(base_url, headers={'User-Agent': random.choice(user_agents_list)})
    find_urls = re.findall(r'(?<=<A HREF=")wspolrzedne_polskich_miejscowosci_.*?\.html(?="><B><FONT face="arial" COLOR)',
                           r.text)
    urls = []
    for url in find_urls:
        urls.append("http://cybermoon.pl/wiedza/wspolrzedne/" + url)

    found_cities = []

    for url in urls:
        r = requests.get(url, headers={'User-Agent': random.choice(user_agents_list)})
        r.encoding = 'ISO-8859-2'
        cities = re.findall(r'(?<=<tr><td><font face="Arial" COLOR=c0c0c0 size=2><b>)(.*?)</td><td>.*?><b>(.*?)'
                            r'</td><td>.*?><b>(.*?) &deg;N&nbsp;&nbsp;</td><td>.*?><b>(.*?)(?= &deg;E</td></tr>)',
                            r.text)
        found_cities += cities

    print(found_cities[0])


def all_cities():
    base_url = "http://cybermoon.pl/wiedza/wspolrzedne/wspolrzedne_polskich_miejscowosci_a.html"
    user_agents_list = [
        'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    ]

    r = requests.get(base_url, headers={'User-Agent': random.choice(user_agents_list)})
    find_urls = re.findall(
        r'(?<=<A HREF=")wspolrzedne_polskich_miejscowosci_.*?\.html(?="><B><FONT face="arial" COLOR)',
        r.text)
    urls = []
    for url in find_urls:
        urls.append("http://cybermoon.pl/wiedza/wspolrzedne/" + url)

    found_cities = []

    for url in urls:
        r = requests.get(url, headers={'User-Agent': random.choice(user_agents_list)})
        r.encoding = 'ISO-8859-2'
        cities = re.findall(r'(?<=<tr><td><font face="Arial" COLOR=c0c0c0 size=2><b>)(.*?)</td><td>.*?><b>(.*?)'
                            r'</td><td>.*?><b>(.*?) &deg;N&nbsp;&nbsp;</td><td>.*?><b>(.*?)(?= &deg;E</td></tr>)',
                            r.text)
        found_cities += cities

    city_data = dict()

    for city in found_cities:
        name = city[0]
        state = city[1]
        lat = city[2]
        lon = city[3]

        if name not in city_data.keys():
            city_data[name] = [(state, lat, lon)]
        else:
            prev = city_data[name]
            prev.append((state, lat, lon))
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

    path = os.getcwd()[:-7] + "/txt Files/biggest_cities.txt"
    f = open(path, 'a')
    for x in biggest_cities_dict.keys():
        line = x + ';\t' + biggest_cities_dict[x][0] + ';\t' + biggest_cities_dict[x][1] + ';\t' + biggest_cities_dict[x][2][0] + ';\t' + biggest_cities_dict[x][2][1] + '\n'
        f.write(line)
    f.close()


def biggest_cities_new_dataset():
    path = os.getcwd()[:-7] + r'\txt Files\Lista-miast-i-miasteczek-w-Polsce.xlsx'
    data = pd.read_excel(path)
    data = data.values.tolist()
    cities = dict()
    for i in range(0, len(data)):
        name, population, lat, lon = data[i]
        if name not in cities.keys() or cities[name][0] < population:
            cities[name] = [population, lat, lon]

    path = os.getcwd()[:-7] + "/txt Files/biggest_cities.txt"
    f = open(path, 'w')
    for x in cities.keys():
        line = x + ';\t' + cities[x][1] + ';\t' + cities[x][2] + '\n'
        f.write(line)
    f.close()


def change_coma_for_dot():
    path = os.getcwd()[:-7] + r'\txt Files\biggest_cities.txt'
    f = open(path, 'r')
    lines = []
    for line in f:
        line = re.sub(',', '.', line)
        lines.append(line)
    f.close()
    f = open(path, 'w')
    for x in lines:
        f.write(x)
    f.close()


#biggest_cities_new_dataset()
#change_coma_for_dot()

#all_cities()

xd()
