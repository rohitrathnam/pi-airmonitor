from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def home():
	con = sql.connect("values.db")

	with con:
		cur = con.execute("SELECT * FROM sensor ORDER BY id DESC LIMIT 1")
	for row in cur:
		print(row)
	return render_template('home.html', rows=row)

@app.route('/status')
def status():
	con = sql.connect("database.db")
	cur = con.execute("select * from settings")
	for row in cur:
		print(row)
	con.close()
	return render_template("status.html",rows = row)

@app.route('/settings')
def settings():
	return render_template("form.html")


@app.route('/change',methods = ['POST', 'GET'])
def change():
	if request.method == 'POST':
		try:
			sv = request.form['sv']
			hv = request.form['hv']
			state = request.form['state']
			with sql.connect("database.db") as con:
				cur = con.cursor()
				cur.execute("UPDATE settings SET state=?, hv=?, sv=? WHERE id=1",(state,hv,sv)) 
				con.commit()
			msg = "Success"
		except:
			con.rollback()
			msg = "Error"

		finally:
			return render_template("result.html",msg = msg)
			con.close()

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug = True)
