def read_file():
    f = open('dane.txt', 'r')
    database = []

    for line in f:
        new_line = line.split(";\t")
        new_line[-1] = new_line[-1][:-1]
        database.append(new_line)
    f.close()
    return database

def change_unknown_and_none_to_null():
    forbidden = ["Unknown", "None", "Brak informacji"]
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] in forbidden:
                data[i][j] = "null"

def save_new_points():
    f = open('dane.txt', 'w')
    for point in data:
        line = ';\t'.join(point)
        line += '\n'
        f.write(line)
    f.close()



data = read_file()
change_unknown_and_none_to_null()
save_new_points()