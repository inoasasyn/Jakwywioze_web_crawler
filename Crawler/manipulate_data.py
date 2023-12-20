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
    i = 1000
    for point in data:
        hours = [';'.join(point[9:]).replace("Zamknięte", "0")]
        if hours == [";;;;;;"]:
            hours = [""]
        line = point + hours + ["True"]
        order = [3, 8, 4, 5, 0, -2, 6, 1, -1, 7, 2]
        line = str(i) + ';\t' + ';\t'.join([line[i] for i in order]) + '\n'
        i += 1
        f.write(line)
    f.close()


def read_ready_file():
    path = os.getcwd()[:-7] + "/txt Files/ready_to_insert.txt"
    f = open(path, 'r')
    database = []

    for line in f:
        new_line = line.split(";\t")
        new_line[-1] = new_line[-1][:-1]
        database.append(new_line)
    f.close()
    return database


def save_ready_file(data):
    path = os.getcwd()[:-7] + "/txt Files/ready_to_insert.txt"
    f = open(path, 'w')
    for line in data:
        line[4], line[3] = line[3], line[4]
        new_line = ';\t'.join(line) + '\n'
        f.write(new_line)
    f.close()


def delete_points():
    path_wt = os.getcwd()[:-7] + r'\txt Files\waste_types.txt'
    path_dane = os.getcwd()[:-7] + r'\txt Files\test_dane'
    to_delete = [84, 70, 67, 65, 64, 59, 54, 51, 50, 49, 48, 45, 42, 41, 40, 39, 38, 34, 32, 31, 23, 17]
    wt = []
    dane = []
    f_wt = open(path_wt, 'r')
    for line in f_wt:
        wt.append(line)
    f_wt.close()
    f_dane = open(path_dane, 'r')
    for line in f_dane:
        dane.append(line)
    f_dane.close()
    deleted = 0
    for i in range(1, len(dane)):
        if i+1 in to_delete:
            dane.remove(dane[i-deleted])
            wt.pop(i-1-deleted)
            deleted += 1
    f_wt = open(path_wt, 'w')
    for line in wt:
        f_wt.write(line)
    f_wt.close()
    f_dane = open(path_dane, 'w')
    for line in dane:
        f_dane.write(line)
    f_dane.close()


data = read_file()
change_unknown_and_none_to_null()
save_new_points()

#data = read_ready_file()
#save_ready_file(data)

#delete_points()
