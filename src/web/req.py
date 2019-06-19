import sqlite3 as sql

def query(qstr):
	con = sql.connect("values.db")
	cur = con.cursor()
	with con:
		con.execute(qstr)
		rows = cur.fetchall();
	print(rows)
