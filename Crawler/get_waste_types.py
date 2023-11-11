import os
import webbrowser
import easyocr


def go_through_websites_1():
    path_dane = os.getcwd()[:-7] + r'\txt Files\test_dane'
    path_wt = os.getcwd()[:-7] + r'\txt Files\waste_types.txt'
    browser_path = "C:/Users/48690/AppData/Local/Programs/Opera GX/launcher.exe %s"
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


def try_text_extraction():
    reader = easyocr.Reader(['pl'])
    path = os.getcwd()[:-7] + r'image.png'
    result = reader.readtext(path)
    for detection in result:
        text = detection[1]
        print(text)


#go_through_websites_1()
#change_website()
try_text_extraction()
