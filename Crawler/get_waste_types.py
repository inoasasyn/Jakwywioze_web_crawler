import os
import webbrowser
import re
import easyocr
from difflib import get_close_matches


DEFAULT_WASTE_TYPES = [
    "przeterminowane leki",
    "odpady wielkogabarytowe",
    "odpady zielone",
    "odpady budowlane, poremontowe i rozbiórkowe",
    "zużyte opony",
    "sprzęt elektryczny i elektroniczny",
    "baterie i akumulatory",
    "opakowania z papieru",
    "opakowania z tektury",
    "odpady opakowaniowe z metali",
    "odpady opakowaniowe z tworzyw sztucznych",
    "szkło opakowaniowe",
    "opakowania z tekstyliów",
    "opakowania zawierające pozostałości substancji niebezpiecznych lub nimi zanieczyszczone",
    "pojemniki pod ciśnieniem po aerozolach",
    "zużyte lub przeterminowane gaśnice samochodowe i z gospodarstw domowych",
    "opony pojazdów osobowych, motocykli, rowerów",
    "beton",
    "gruz betonowy",
    "gruz ceglany",
    "zmieszane odpady z betonu, gruzu ceglanego, ceramiki, glazury, terakoty itp.",
    "szkło okienne, drzwiowe, bezbarwne, lustra",
    "odzież",
    "tekstylia",
    "rozpuszczalniki",
    "kwasy",
    "alkalia (substancje żrące)",
    "odczynniki fotograficzne",
    "środki ochrony roślin",
    "świetlówki",
    "termometry rtęciowe",
    "urządzenia chłodnicze i klimatyzacyjne",
    "oleje spożywcze",
    "oleje silników samochodowych",
    "farby",
    "farby drukarskie",
    "tusze",
    "tonery do drukarek",
    "kleje",
    "lepiszcze",
    "żywice",
    "detergenty",
    "leki",
    "telewizory, monitory",
    "małe i duże urządzenia elektryczne i elektroniczne"
    "drewno",
    "odpady tworzyw sztucznych",
    "odpady metali",
    "odpady komunalne"
]


def go_through_websites_1():
    path_dane = os.getcwd()[:-7] + r'\txt Files\test_dane'
    path_wt = os.getcwd()[:-7] + r'\txt Files\waste_types.txt'
    f = open(path_dane, 'r')
    lines = []
    for line in f:
        line = line.split(';\t')
        line[-1] = line[-1][:-1]
        lines.append(line)
    f.close()

    waste_types = []
    f = open(path_wt, 'r')
    for line in f:
        waste_types.append(line[:-1])
    f.close()

    browser_path = "C:/Users/48690/AppData/Local/Programs/Opera GX/launcher.exe %s"
    for line in lines[1+len(waste_types):]:
        url = line[7]
        if url != "None":
            print(line)
            webbrowser.get(browser_path).open(url)
            is_info_on_site = input("Status: ")
            if is_info_on_site == '1':
                f = open(path_wt, 'a')
                f.write("in html\n")
                f.close()
            elif is_info_on_site == '2':
                f = open(path_wt, 'a')
                f.write("on site, but not in html\n")
                f.close()
            elif is_info_on_site == '3':
                new_web = input("Nowy adres strony: ")
                line[7] = new_web
                new_web += '\n'
                f = open(path_wt, 'a')
                f.write("change site to; ")
                f.write(new_web)
                f.close()
            else:
                f = open(path_wt, 'a')
                f.write("no info\n")
                f.close()
        else:
            f = open(path_wt, 'a')
            f.write("default\n")
            f.close()


def change_website():
    path_dane = os.getcwd()[:-7] + r'\txt Files\test_dane'
    path_wt = os.getcwd()[:-7] + r'\txt Files\waste_types.txt'
    f = open(path_wt, 'r')
    wt = []
    for line in f:
        line = line.split('; ')
        line[-1] = line[-1][:-1]
        wt.append(line)
    f.close()
    f = open(path_dane, 'r')
    dane = []
    for line in f:
        line = line.split(';\t')
        line[-1] = line[-1][:-1]
        dane.append(line)
    f.close()
    for i in range(len(wt)):
        if len(wt[i]) > 1:
            dane[i+1][7] = wt[i][1]
            print(dane[i+1])
    f = open(path_dane, 'w')
    for i in range(len(dane)):
        line = ';\t'.join(dane[i])
        line += '\n'
        f.write(line)
    f.close()


def using_polimorf():
    path_dane = os.getcwd()[:-7] + r'PoliMorf-0.6.7.tab'
    file_in = open(path_dane, 'r', encoding='utf8')
    lines_in = file_in.readlines()
    polish_dict = {}
    for line in lines_in:
        x = line.split()
        word = x[0]
        if len(word) not in polish_dict.keys():
            polish_dict[len(word)] = {word}
        else:
            prev = polish_dict[len(word)]
            prev.add(word)
            polish_dict[len(word)] = prev

    alphabet = ['a', 'ą', 'b', 'c', 'ć', 'd', 'e', 'ę', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'ł', 'm', 'n', 'ń', 'o',
                'ó', 'p', 'q', 'r', 's', 'ś', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ź', 'ż']
    while True:
        user_string = input("Podaj słowo do analizy: ")
        word = user_string.lower()
        guess = get_close_matches(user_string, polish_dict[len(user_string)], n=len(user_string))
        rates = []
        for x in guess:
            score = 0
            for i in range(len(word)):
                if word[i] == x[i]:
                    score += 1
            rates.append(score)
        result = [guess[i] for i in range(len(guess)) if rates[i] == max(rates)]
        print(result)


def get_img():
    path_dane = os.getcwd()[:-7] + r'\txt Files\test_dane'
    path_wt = os.getcwd()[:-7] + r'\txt Files\waste_types.txt'
    f = open(path_wt, 'r')
    wt = []
    lines = []
    for line in f:
        lines.append(line)
        line = line.split('; ')
        line[-1] = line[-1][:-1]
        wt.append(line)
    f.close()
    f = open(path_dane, 'r')
    dane = []
    for line in f:
        line = line.split(';\t')
        line[-1] = line[-1][:-1]
        dane.append(line)
    f.close()

    browser_path = "C:/Users/48690/AppData/Local/Programs/Opera GX/launcher.exe %s"
    reader = easyocr.Reader(['pl'])
    for i in range(len(wt)):
        if wt[i][0] in ["change site to", "in html", "on site, but not in html"]:
            url = dane[i+1][7]
            webbrowser.get(browser_path).open(url)
            user_input = input("Press to continue")
            path = os.getcwd()[:-7] + r'image.png'
            result = reader.readtext(path)
            line_in = ""
            for detection in result:
                text = re.sub('\n', '', detection[1])
                line_in += ";\t" + str(text)
            print(line_in)
            line_in += '\n'
            lines[i] = line_in
            f = open(path_wt, 'w')
            for line in lines:
                f.write(line)
            f.close()


def correct_common_mistakes():
    mistakes = {
        ";;": ";",
        "zuzyte": "zużyte",
        "; ": ", ",
        "i;\t": "i ",
        "odziez": "odzież",
        ",;": ";"
    }
    path_wt = os.getcwd()[:-7] + r'\txt Files\waste_types.txt'
    wt = []
    f = open(path_wt, 'r')
    for line in f:
        line = line[:-1]
        wt.append(line)
    f.close()
    new_wt = []
    for line in wt:
        line = line.lower()
        for m in mistakes.keys():
            line = re.sub(m, mistakes[m], line)
        new_wt.append(line)
    f = open(path_wt, 'w')
    for line in new_wt:
        line += '\n'
        f.write(line)
    f.close()


def create_files_to_insert():
    path_wt = os.getcwd()[:-7] + r'\txt Files\waste_types.txt'
    point_waste = {}
    wt = {}
    f = open(path_wt, 'r')
    wt_counter = 0
    point_counter = 0
    for line in f:
        point_waste[point_counter] = []
        line = line.split(';')
        line[-1] = line[-1][:-1]
        # adding default
        if len(line) == 1:
            line = ["default"] + DEFAULT_WASTE_TYPES
        for i in range(1, len(line)):
            line[i] = line[i].lstrip()
            if line[i] not in wt.keys():
                wt[line[i]] = wt_counter
                wt_counter += 1
            current = point_waste[point_counter]
            current.append(wt[line[i]])
            point_waste[point_counter] = sorted(current)
        point_counter += 1
    f.close()

    path_db_wt = os.getcwd()[:-7] + r'\txt Files\DB_waste_types.txt'
    path_db_point_waste = os.getcwd()[:-7] + r'\txt Files\DB_point_waste.txt'
    f = open(path_db_wt, 'w')
    for k in wt.keys():
        line = str(wt[k]) + ";\t" + str(k) + "\n"
        f.write(line)
    f.close()
    f = open(path_db_point_waste, 'w')
    for i in range(len(point_waste)):
        for j in range(len(point_waste[i])):
            line = str(1000+i) + ";" + str(point_waste[i][j]) + "\n"
            f.write(line)
    f.close()


#go_through_websites_1()
#change_website()
#try_text_extraction()
#using_polimorf()
#get_img()
#correct_common_mistakes()
create_files_to_insert()
