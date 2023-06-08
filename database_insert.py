import psycopg2
import re



def read_file():

    f = open('dane.txt', 'r')
    points = []
    waste_types = []

    for line in f:
        new_line = line.split(";\t")
        new_line[-1] = new_line[-1][:-1]
        new_line = new_line[:9] + [';'.join(new_line[9:]).replace("Zamknięte", "0")]
        order = []
        order.append(new_line[3])
        order.append(new_line[5])
        order.append(new_line[4])
        order.append(new_line[0])
        order.append(new_line[-1])
        order.append(new_line[1])
        order.append('True')
        points.append(tuple(order))

    f.close()
    return points[2:]

def insert_point_list(points_list):
    sql = "INSERT INTO point (city, lat, lon, name, opening_hours, street, type) VALUES(%s, %s, %s, %s, %s, %s, %s)"
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