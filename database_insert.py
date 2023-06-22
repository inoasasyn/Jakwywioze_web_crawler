import psycopg2
import random



waste_types = [
    "przeterminowane leki",
    "odpady wielkogabarytowe",
    "odpady zielone",
    "odpady budowlane, poremontowe i rozbiórkowe",
    "zużyte opony",
    "elektrośmieci, czyli sprzęt elektryczny i elektroniczny",
    "baterie i akumulatory",
    "opakowania z papieru i tektury",
    "odpady opakowaniowe z metali i tworzyw sztucznych",
    "szkło opakowaniowe",
    "opakowania z tekstyliów",
    "opakowania zawierające pozostałości substancji niebezpiecznych lub nimi zanieczyszczone",
    "pojemniki pod ciśnieniem po aerozolach, zużyte lub przeterminowane gaśnice samochodowe i z gospodarstw domowych",
    "opony pojazdów osobowych, motocykli, rowerów",
    "beton oraz gruz betonowy",
    "gruz ceglany",
    "zmieszane odpady z betonu, gruzu ceglanego, ceramiki, glazury, terakoty itp.",
    "szkło okienne, drzwiowe, bezbarwne, lustra",
    "odzież",
    "tekstylia",
    "rozpuszczalniki",
    "kwasy",
    "alkalia (substancje żrące)",
    "odczynniki fotograficzne",
    "środki ochrony roślin zawierające substancje niebezpieczne",
    "świetlówki, świetlówki energooszczędne",
    "termometry rtęciowe",
    "urządzenia chłodnicze i klimatyzacyjne, np.: lodówki, chłodziarki, klimatyzatory domowe",
    "oleje spożywcze (przeterminowane zużyte)",
    "przepracowane lub przeterminowane oleje silników samochodowych",
    "farby, farby drukarskie, tusze, tonery do drukarek zawierające substancje niebezpieczne",
    "kleje, lepiszcze i żywice zawierające substancje niebezpieczne",
    "farby, farby drukarskie, tusze, tonery do drukarek",
    "kleje, lepiszcze i żywice",
    "detergenty zawierające substancje niebezpieczne",
    "detergenty",
    "leki",
    "akumulatory i baterie",
    "telewizory, monitory",
    "małe i duże urządzenia elektryczne i elektroniczne",
    "drewno zawierające substancje niebezpieczne",
    "drewno, tj. skrzynki drewniane, deski itp.",
    "odpady tworzyw sztucznych, np. wiadra, miski, zabawki, skrzynki, meble ogrodowe itp.",
    "odpady metali, np. ramy rowerowe, koła rowerowe, wieszaki, obudowy urządzeń, klamki, elementy metalowe itp.",
    "środki ochrony roślin niezawierające substancji niebezpiecznych",
    "inne odpady komunalne",
    "odpady wielkogabarytowe – meble",
    "odpady wielkogabarytowe – materace"
]

def generate_point_waste_type(points_list):
    pwt_list = []
    for i in range(1, len(points_list)-1):
        n = random.randint(1, len(waste_types) - 28)
        temp = random.sample(range(1, len(waste_types)), n)
        for j in temp:
            pwt_list.append([i+1, j])
    for i in range(len(waste_types)):
        pwt_list.append([1, i+1])
    return pwt_list

def read_file():

    f = open('dane.txt', 'r')
    points = []
    #Name;	Street;	Zip;	City;	Longitude;	Latitude;	Phone;	Web;	PhotoLink;	Monday;	Tuesday;	Wednesday;	Thursday;	Friday;	Saturday;	Sunday

    for line in f:
        new_line = line.split(";\t")
        new_line[-1] = new_line[-1][:-1]
        hours = [';'.join(new_line[9:]).replace("Zamknięte", "0")]
        if hours == [";;;;;;"]:
            hours = [""]
        new_line = new_line[:9] + hours + ["True"]
        order = [3, 8, 5, 4, 0, 9, 6, 1, 10, 7, 2]
        point = [new_line[i] for i in order]
        points.append(tuple(point))

    f.close()
    return points[1:]

def insert_point_list(points_list):
    sql_point = "INSERT INTO point (city, image_link, lat, lon, name, opening_hours, phone_number, street, type, website, zipcode) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    sql_waste_type = "INSERT INTO waste_type (id, name) VALUES(%s, %s)"
    sql_pt_wt = "INSERT INTO point_waste (point_id, waste_type_id) VALUES(%s, %s)"

    conn = None
    try:
        conn = psycopg2.connect(
            dbname='jakwywioze', user='jakwywioze', password='jakwywioze', host='localhost', port='5432'
        )
        conn.autocommit = True
        cur = conn.cursor()
        for i in range(len(waste_types)):
            waste_types[i] = [i+1] + [waste_types[i]]
        cur.executemany(sql_waste_type, waste_types)
        cur.executemany(sql_point, points_list)
        cur.executemany(sql_pt_wt, pwt)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



database = read_file()
pwt = generate_point_waste_type(database)
insert_point_list(database)