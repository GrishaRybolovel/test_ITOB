import sqlite3
import datetime

def connect_sql():

    conn = None

    try:
        conn = sqlite3.connect('sqlitedb.db')
        conn.row_factory = sqlite3.Row
        if conn:
            print('Database successfully connected!')
    except Exception as e:
        print(str(e))

    #cur.execute("DROP TABLE IF EXISTS auth")
    # cur.execute("DROP TABLE IF EXISTS models")
    # cur.execute("DROP TABLE IF EXISTS tickets_to_show")
    # cur.execute("DROP TABLE IF EXISTS profiles")
    # cur.execute("DROP TABLE IF EXISTS tickets")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS log (id SERIAL PRIMARY KEY, message VARCHAR, ttime VARCHAR);"
    )

    conn.commit()

    return conn


def add_message(conn, message):
    cur = conn.cursor()
    cur.execute('INSERT INTO log (message, ttime) VALUES (?, ?)', (message, str(datetime.datetime.now())))

    conn.commit()