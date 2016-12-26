import fileinput
import os.path
import sqlite3


def get_logs_path(path):
    files = list()
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in [f for f in filenames if f.endswith(".log")]:
            files.append(os.path.join(dirpath, filename))
    return files


def create_db(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Logs')
    cur.execute('''CREATE TABLE Logs (month TEXT, day INTEGER, time TEXT,
        operation TEXT, path TEXT, fruit TEXT, hex_code TEXT, value INTEGER)''')
    for line in sorted((fileinput.input(get_logs_path('.')))):
        line = tuple(line.split())
        cur.execute('''INSERT INTO Logs (month, day, time, operation, path, fruit, hex_code, value) VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?)''', line)
    conn.commit()
    conn.close()


def retrieve_kiwi_data(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('SELECT MAX(value), MIN(value), AVG(value) from Logs WHERE fruit = "Kiwi"')
    for row in cur:
        print 'Max Kiwi:', row[0]
        print 'Min Kiwi:', row[1]
        print 'Average Kiwi:', row[2]
    conn.close()


create_db('all_logs.sqlite3')
retrieve_kiwi_data('all_logs.sqlite3')