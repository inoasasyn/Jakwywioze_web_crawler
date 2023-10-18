import os


def read_file():
    path = os.getcwd()[:-7] + "/txt Files/test_dane"
    f = open(path, 'r')
    database = []

    for line in f:
        new_line = line.split(";\t")
        new_line[-1] = new_line[-1][:-1]
        database.append(new_line)
    f.close()
    return database[1:]


def change_unknown_and_none_to_null():
    forbidden = ["Unknown", "Unnamed Road", "None", "Brak informacji", "null"]
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] in forbidden:
                data[i][j] = ""


def save_new_points():
    path = os.getcwd()[:-7] + "/txt Files/ready_to_insert.txt"
    f = open(path, 'w')
    for point in data:
        line = ';\t'.join(point[:9])
        hours = [';'.join(point[9:]).replace("Zamknięte", "0")]
        if hours == [";;;;;;"]:
            hours = [""]
        line = line + ';\t' + hours[0] + '\n'
        f.write(line)
    f.close()


data = read_file()
change_unknown_and_none_to_null()
save_new_points()
