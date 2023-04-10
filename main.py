from urllib.request import urlopen
import re
import time
from bs4 import *
import requests
import pandas as pd



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


def all_pszoks_noapi():

    urls = all_cities()
    #urls = ["https://www.google.com/maps/search/pszok+wielkopolska/"]
    data_file = open('dane.txt', 'a')
    database = read_file()

    for url in urls:

        print(url)
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        html = re.sub("&nbsp;", " ", html)

        #[\"PSZOK Punkt selektywnej zbiórki odpadów komunalnych, Lotnicza 33a, 63-410 Ostrów Wielkopolski\"]

        pattern_results = re.findall(r'(?<=\[\\")[A-ZŻŹĆĄŚĘŁÓŃa-zżźćńółęąś\s-]+, [0-9A-ZŻŹĆĄŚĘŁÓŃa-zżźćńółęąś\s-]+, [0-9A-ZŻŹĆĄŚĘŁÓŃa-zżźćńółęąś\s-]+(?=\\"])', html)

        for x in pattern_results:
            d = re.split(", ", x)
            if d[1] != 'Unnamed Road' or re.search('[A-ZŻŹĆĄŚĘŁÓŃa-zżźćńółęąś]', d[2]):
                if " " in d[2]:
                    zip, city = d[2].split(" ", 1)
                else:
                    zip = d[2]
                    city = "Unknown"
                d = d[:2]
                d.append(zip)
                d.append(city)
                if d not in database:
                    database.append(d)
                    data_file.write(str(d[0]) + ";" + "\t" + str(d[1]) + ";" + "\t" + str(zip) + ";" + "\t" + str(city) + "\n")

        time.sleep(73)

    data_file.close()



def read_file():

    f = open('dane.txt', 'r')
    database = []

    for line in f:
        d = re.split(";\t", line)
        d[3] = d[3][:-1]
        database.append(d)

    f.close()
    return database



def pszok_addresses():

    urls = ["https://www.zzo.pl/pl/o-nas/informacje-ogolne/10-pl/zakres-dzialalnosci/6-punkt-selektywnego-zbierania-odpadow-komunalnych-gratowisko",
            "http://uk-sroda.pl"]

    url = "https://www.zzo.pl/pl/o-nas/informacje-ogolne/10-pl/zakres-dzialalnosci/6-punkt-selektywnego-zbierania-odpadow-komunalnych-gratowisko"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    html = re.sub("&nbsp;", " ", html)
    #print(html)

    patterns = ['ul\..*?[0-9]+\sw\s[A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćńółęąś]+',
                'ul\..*?[0-9]+\sw\s[A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćńółęąś]+\s[A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćńółęąś]+',
                'ul\..*?[0-9]+\sw\s[A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćńółęąś]+\s[A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćńółęąś]+\s[A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćńółęąś]+',
                'ul\..*?[0-9]+\s[0-9][0-9]-[0-9][0-9][0-9]\s[A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćńółęąś]+',
                'ul\..*?[0-9]+\s[0-9][0-9]-[0-9][0-9][0-9]\s[A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćńółęąś]+\s[A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćńółęąś]+',
                'ul\..*?[0-9]+\s[0-9][0-9]-[0-9][0-9][0-9]\s[A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćńółęąś]+\s[A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćńółęąś]+\s[A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćńółęąś]+'
                ]
    addresses = []

    for x in patterns:
        pattern_results = re.findall(x, html)
        for y in pattern_results:
            if y.count("ul.") == 1:
                addresses.append(y)
            else:
                all_ul = re.finditer(r"ul.", y)
                start_ul = 0
                for i in all_ul:
                    start_ul = i.start()
                new_address = y[start_ul:]
                for i in addresses:
                    if i in new_address:
                        addresses.remove(i)
                addresses.append(new_address)

    print(addresses)



all_pszoks_noapi()