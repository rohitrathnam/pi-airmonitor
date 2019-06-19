import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

#conn.execute('CREATE TABLE settings (id INTEGER, state TEXT, hv REAL, sv REAL)')
print("Table created successfully")

conn.execute('INSERT INTO settings (id, state, hv, sv) VALUES (1, "On", 2.5, 5.5)')
conn.commit()
conn.close()
