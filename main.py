from urllib.request import urlopen
import re
from bs4 import *
import requests
import pandas as pd
import time



def all_cities():

    wikiurl = "https://pl.wikipedia.org/wiki/Miasta_w_województwie_wielkopolskim"
    table_class = "wikitable sortable jquery-tablesorter"
    response = requests.get(wikiurl)
    soup = BeautifulSoup(response.text, 'html.parser')
    indiatable = soup.find('table', {'class': "wikitable"})
    df = pd.read_html(str(indiatable))
    df = pd.DataFrame(df[0])
    data = df.drop(["Pozycja", "Herb", "Ludność", "Pow.(km²)", "Gęst. zal.(os./km²)", "Powiat"], axis=1)

    polish_letters_replace = {
        ' ': '+',
        'ę': 'e',
        'ó': 'o',
        'ą': 'a',
        'ś': 's',
        'ł': 'l',
        'ż': 'z',
        'ź': 'z',
        'ć': 'c',
        'ń': 'n',
        'Ę': 'E',
        'Ó': 'E',
        'Ą': 'A',
        'Ś': 'S',
        'Ł': 'L',
        'Ż': 'Z',
        'Ź': 'Z',
        'Ć': 'C',
        'Ń': 'N'
    }

    urls = ["https://www.google.com/maps/search/pszok+wielkopolska/"]

    for x in data["Miasto"]:
        city_plus = str(x)
        for pattern in polish_letters_replace:
            city_plus = re.sub(pattern, polish_letters_replace[pattern], city_plus)
        if city_plus != "nan":
            url = "https://www.google.com/maps/search/pszok+" + city_plus + "/"
            urls.append(url)

    return urls


def read_file():

    f = open('dane.txt', 'r')
    database = []

    for line in f:
        database.append(line)

    f.close()
    return database


def split_address(add):
    name_address = add.split(sep=", ")
    name = ", ".join(name_address[:-2])
    street = name_address[-2]
    if name == "":
        name = street
        street = "Unknown"
    if " " in name_address[-1]:
        zip, city = name_address[-1].split(" ", 1)
    else:
        zip = name_address[-1]
        city = "Unknown"
    return [name, street, zip, city]


def split_hours(days):
    hours = []
    for day in days:
        if len(day) > 0:
            current_day = day[0]
            if current_day[-2] != '2':
                current_day = re.findall(r'[0-9]{2}:[0-9]{2}.*?[0-9]{2}:[0-9]{2}', current_day)[0]
            else:
                current_day = "Zamknięte"
            hours.append(current_day)
        else:
            hours.append("Brak informacji")
    return hours

def try_one():
    url = "https://www.google.com/maps/search/pszok+wielkopolska/"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    html = re.sub("&nbsp;", " ", html)
    html = re.sub("2,null,0", "1,[[9,9,9,9]],0", html)

    points = []
    points.append(["Name", "Street", "Zip", "City", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    pattern_point_results = re.findall(r'\[\[\[7,\[\[\\".*?\[\[null,null,[0-9]+\.[0-9]+,[0-9]+\.[0-9]+]]', html)

    pattern_hours = []

    for point in pattern_point_results:

        add = re.findall(r'(?<=\[2,\[\[\\").*?, [0-9]{2}-[0-9]{3}.*?\\"]]]', point)
        new_point = split_address(add[0][:-5])

        pon = re.findall(r'\[\\"poniedziałek\\",1,\[.*?,.*?,.*?],\[\[\\".*?]],0,[1-2]]', point)
        wt = re.findall(r'\[\\"wtorek\\",2,\[.*?,.*?,.*?],\[\[\\".*?]],0,[1-2]]', point)
        sr = re.findall(r'\[\\"środa\\",3,\[.*?,.*?,.*?],\[\[\\".*?]],0,[1-2]]', point)
        czw = re.findall(r'\[\\"czwartek\\",4,\[.*?,.*?,.*?],\[\[\\".*?]],0,[1-2]]', point)
        pt = re.findall(r'\[\\"piątek\\",5,\[.*?,.*?,.*?],\[\[\\".*?]],0,[1-2]]', point)
        so = re.findall(r'\[\\"sobota\\",6,\[.*?,.*?,.*?],\[\[\\".*?]],0,[1-2]]', point)
        nd = re.findall(r'\[\\"niedziela\\",7,\[.*?,.*?,.*?],\[\[\\".*?]],0,[1-2]]', point)
        days = [pon, wt, sr, czw, pt, so, nd]
        hours = split_hours(days)

        new_point = new_point + hours
        points.append(new_point)

    print(points)


def write_file(point):
    f = open("dane.txt", "a")
    f.write(point)
    f.close()


def get_points():
    #urls = all_cities()
    urls = ['https://www.google.com/maps/search/pszok+wielkopolska/']
    database = read_file()
    points = []
    points.append(["Name", "Street", "Zip", "City", "Longitude", "Latitude", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    title_line = ';\t'.join(points[0])
    title_line += '\n'
    if database == [] or database[0] != title_line:
        with open('dane.txt', 'r') as original: data = original.read()
        with open('dane.txt', 'w') as modified: modified.write(title_line + data)

    for url in urls:
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        html = re.sub("&nbsp;", " ", html)
        html = re.sub("2,null,0", "1,[[9,9,9,9]],0", html)

        pattern_point_results = re.findall(r'\[\[\[7,\[\[\\".*?\[\[null,null,[0-9]+\.[0-9]+,[0-9]+\.[0-9]+]]', html)

        for point in pattern_point_results:

            add = re.findall(r'(?<=\[2,\[\[\\").*?, [0-9]{2}-[0-9]{3}.*?\\"]]]', point)
            new_point = split_address(add[0][:-5])

            geo_loc = re.findall(r'\[\[null,null,[0-9]+\.[0-9]+,[0-9]+\.[0-9]+]]', point)[0]
            geo_loc = re.split(",", geo_loc[2:-2])
            longitude = geo_loc[2]
            latitude = geo_loc[3]
            new_point = new_point + [longitude, latitude]

            pon = re.findall(r'\[\\"poniedziałek\\",1,\[.*?,.*?,.*?],\[\[\\".*?]],0,[1-2]]', point)
            wt = re.findall(r'\[\\"wtorek\\",2,\[.*?,.*?,.*?],\[\[\\".*?]],0,[1-2]]', point)
            sr = re.findall(r'\[\\"środa\\",3,\[.*?,.*?,.*?],\[\[\\".*?]],0,[1-2]]', point)
            czw = re.findall(r'\[\\"czwartek\\",4,\[.*?,.*?,.*?],\[\[\\".*?]],0,[1-2]]', point)
            pt = re.findall(r'\[\\"piątek\\",5,\[.*?,.*?,.*?],\[\[\\".*?]],0,[1-2]]', point)
            so = re.findall(r'\[\\"sobota\\",6,\[.*?,.*?,.*?],\[\[\\".*?]],0,[1-2]]', point)
            nd = re.findall(r'\[\\"niedziela\\",7,\[.*?,.*?,.*?],\[\[\\".*?]],0,[1-2]]', point)
            days = [pon, wt, sr, czw, pt, so, nd]
            hours = split_hours(days)

            new_point = new_point + hours
            line = ';\t'.join(new_point)
            line += '\n'
            points.append(new_point)

            if line not in database:
                database.append(line)
                write_file(line)

        #time.sleep(120)



get_points()