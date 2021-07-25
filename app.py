import datetime
from flask import Flask,render_template,request,url_for
import sqlite3 as sql

app=Flask(__name__)
@app.route('/',methods = ['GET'])
def index():
    if request.method == "GET":

        with sql.connect("database.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("select * from todo")
            rows = cur.fetchall();
            return render_template("index.html", rows=rows)

    else:
        msg="Nothing"
        return render_template('index.html', msg=msg)


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':

        try:
            title = request.form['title']
            desc = request.form['des']
            da = datetime.datetime.now()
            with sql.connect("database.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO todo (title,description,date) VALUES('{t}','{d}','{dd}')".format(t=title,d=desc,dd=da))

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()



if __name__=='__main__':
    app.run(debug=True)