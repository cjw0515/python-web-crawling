import sqlite3 as lite
import time

database_filename = 'test.db'
conn = lite.connect(database_filename)
cs = conn.cursor()

#drop table
query = "DROP TABLE IF EXISTS t1"
cs.execute(query)



#create table
query = """CREATE TABLE IF NOT EXISTS t1 (
id INTEGER PRIMARY_KEY NOT_NULL
, name VARCHAR(255)
, at DATETIME
)"""
cs.execute(query)

#insert table
chars = "abcdefghijklmnopqrstuvwxyz"
for a in range(len(chars)):
    query = "INSERT into t1 values (?, ? , DATETIME('NOW'))"
    cs.execute(query,(a, chars[a]))
conn.commit()
# closig
cs.close()
conn.close()