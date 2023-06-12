import psycopg2



def read_file():

    f = open('dane.txt', 'r')
    points = []
    waste_types = []
    #Name;	Street;	Zip;	City;	Longitude;	Latitude;	Phone;	Web;	PhotoLink;	Monday;	Tuesday;	Wednesday;	Thursday;	Friday;	Saturday;	Sunday

    for line in f:
        new_line = line.split(";\t")
        new_line[-1] = new_line[-1][:-1]
        new_line = new_line[:9] + [';'.join(new_line[9:]).replace("Zamknięte", "0")] + ["True"]
        order = [3, 8, 5, 4, 0, 9, 6, 1, 10, 7, 2]
        point = [new_line[i] for i in order]
        points.append(tuple(point))

    f.close()
    return points[2:]

def insert_point_list(points_list):
    sql = "INSERT INTO point (city, image_link, lat, lon, name, opening_hours, phone_number, street, type, website, zipcode) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    conn = None
    try:
        conn = psycopg2.connect(
            dbname='jakwywioze', user='jakwywioze', password='jakwywioze', host='localhost', port='5432'
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.executemany(sql, points_list)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

database = read_file()
#print(database)
insert_point_list(database)