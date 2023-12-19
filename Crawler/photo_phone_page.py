import webbrowser
import os

browser_path = "C:/Users/48690/AppData/Local/Programs/Opera GX/launcher.exe %s"


def read_file():
    path = os.getcwd() + "/txt Files/test_dane"
    f = open(path, 'r')
    database = []

    for line in f:
        new_line = line.split(";\t")
        new_line[-1] = new_line[-1][:-1]
        database.append(new_line)

    f.close()
    return database


def save_new_points(points):
    path = os.getcwd() + "/txt Files/test_dane"
    f = open(path, 'w')
    for point in points:
        line = ';\t'.join(point)
        line += '\n'
        f.write(line)
    f.close()

#https://www.google.com/maps/@?api=1&map_action=map&center=52.214954%2C17.28614349999999
#https://www.google.com/maps/@?api=1&map_action=map&center=52.642345299999995%2C16.5921084


def open_urls_and_read_input():

    new_data = data.copy()

    for i in range(len(data)):
        if len(data[i]) != 16:
            if i == 0:
                new_title = data[i][:6] + ["Phone", "Web", "PhotoLink"] + data[i][6:]
                new_data[i] = new_title
            else:
                long, lat = data[i][4], data[i][5]
                url = "https://www.google.com/maps/@?api=1&map_action=map&center=" + str(long) + "%2C" + str(lat)
                print(url)
                print(data[i])
                webbrowser.get(browser_path).open(url)
                phone = input("Podaj numer telefonu: ")
                web = input("Podaj stronę internetową: ")
                photo = input("Podaj link do zdjęcia: ")
                target = photo.rfind("=")
                if target != -1:
                    new_photo = photo[:target] + "=s0"
                else:
                    new_photo = "None"

                new_point = data[i][:6] + [phone, web, new_photo] + data[i][6:]
                print(new_point)
                new_data[i] = new_point

        save_new_points(new_data)
    return new_data


data = read_file()
new_data = open_urls_and_read_input()
save_new_points(new_data)
