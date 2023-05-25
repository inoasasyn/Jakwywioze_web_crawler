import psycopg2



def read_file():

    f = open('dane.txt', 'r')
    database = []

    for line in f:
        new_line = line.split(";\t")
        new_line[-1] = new_line[-1][:-1]
        new_line = new_line[:6] + ['; '.join(new_line[6:])]
        order = []
        order.append(new_line[3])
        order.append(new_line[5])
        order.append(new_line[4])
        order.append(new_line[0])
        order.append(new_line[-1])
        order.append(new_line[1])
        order.append('True')
        database.append(tuple(order))

    f.close()
    return database[2:]

def insert_point_list(vendor_list):
    """ insert multiple vendors into the vendors table  """
    sql = "INSERT INTO point (city, lat, lon, name, opening_hours, street, type) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    conn = None
    try:
        conn = psycopg2.connect(
            dbname='postgres', user='postgres', password='postgres', host='localhost', port='5432'
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.executemany(sql, vendor_list)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

database = read_file()
insert_point_list(database)