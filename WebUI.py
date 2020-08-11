import SNMP
from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

@app.route("/")
def flaskss007():
    try:
        con = sql.connect("Monitor_DB.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select * from Monitor_Table")
        z = cur.fetchall()
        return render_template("1.html", z=z)
    except Exception as e:
        SNMP.write_to_log002(f"Fail Error: 007 -- {e}")
        SNMP.send_email003()
@app.route("/add")
def add_new_monitoring_web008():
    try:
        return render_template("2.html")
    except Exception as e:
        SNMP.write_to_log002(f"Fail Error: 008 -- {e}")
        SNMP.send_email003()
@app.route('/add_rec009',methods = ['POST', 'GET'])
def add_rec009():
    if request.method == 'POST':
        try:
            if not request.form.getlist('ping'):
                p = "0"
            else:
                p = allow_ping010(request.form['ping'])

            if not request.form.getlist('snmp'):
                s = "0"
            else:
                s = allow_snmp011()(request.form['snmp'])
            a = request.form['ip']
            po = request.form['Num1']
            print(type(po))

            with sql.connect("Monitor_DB.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Monitor_Table (IPorDNS, PORT, PING, SNMP)\
                VALUES(?, ?, ?, ?)", (a, po, p, s))
                con.commit()
                msg = "Record successfully added"
        except Exception as e:
            con.rollback()
            msg = "error in insert operation"
            SNMP.write_to_log002(f"Fail Error: 006 -- {e}")
            SNMP.send_email003()

        finally:
            return render_template("result.html", msg=msg)
            con.close()
def allow_ping010(p):
    try:
        if p == "ping":
            return "1"
        else:
            return "0"
    except Exception as e:
        SNMP.write_to_log002(f"Fail Error: 010 -- {e}")
        SNMP.send_email003()
def allow_snmp011(s):
    try:
        if s == "snmp":
            return "1"
        else:
            return "0"
    except Exception as e:
        SNMP.write_to_log002(f"Fail Error: 011 -- {e}")
        SNMP.send_email003()

if __name__ == "__main__":
    app.run()