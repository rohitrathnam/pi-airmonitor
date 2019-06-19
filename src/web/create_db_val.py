import sqlite3

conn = sqlite3.connect('values.db')
print("Opened database successfully")

conn.execute('CREATE TABLE sensor (id INTEGER PRIMARY KEY AUTOINCREMENT, time DATETIME DEFAULT CURRENT_TIMESTAMP, co2 REAL, temp REAL, hum REAL)')
print("Table created successfully")

#conn.execute('INSERT INTO sensor (co2, temp, hum) VALUES (2.5, 5.5, 7.5)')
#conn.execute('INSERT INTO sensor (co2, temp, hum) VALUES (3, 4.5, 8.5)')
#conn.execute('INSERT INTO sensor (co2, temp, hum) VALUES (2.5, 6.5, 2.5)')
conn.commit()
conn.close()
