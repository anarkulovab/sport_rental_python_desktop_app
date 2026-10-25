import pymysql as psql

try:
    conn = psql.connect(host="localhost", user="root", password="root", database="sport_rental")
    print("BD connect OK")
except Exception as e:
    print(e)


def select_query(sql, params=None):
    cursor = conn.cursor()
    if params:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
    return res


def update_query(sql, params=None):
    cursor = conn.cursor()
    if params:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)
    conn.commit()
    cursor.close()