from flask import Flask, render_template, request, jsonify, redirect, session
import sqlite3, hashlib, os
from datetime import datetime

app = Flask(__name__)
app.secret_key="blackbox_v6"

BASE=os.path.dirname(os.path.abspath(__file__))
DB=os.path.join(BASE,"blackbox.db")

def db():
    return sqlite3.connect(DB,check_same_thread=False)

def init_db():

    print("Creating DB at:",DB)

    con=db()
    cur=con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS scans(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    score INTEGER,
    critical INTEGER,
    high INTEGER,
    medium INTEGER,
    low INTEGER,
    issues TEXT,
    time TEXT)""")

    con.commit()
    con.close()

init_db()

def analyze(code):

    critical=high=medium=low=0
    issues=[]

    if "select" in code and "+" in code:
        critical+=1; issues.append("SQL Injection")

    if "<script>" in code:
        high+=1; issues.append("XSS")

    if "password" in code:
        medium+=1; issues.append("Hardcoded Secret")

    if "eval(" in code:
        critical+=1; issues.append("Unsafe Eval")

    score=min(critical*40+high*25+medium*20+low*10,100)

    return score,critical,high,medium,low,issues

@app.route("/")
def home():
    if "user" not in session: return redirect("/login")
    return render_template("index.html",user=session["user"])

@app.route("/signup",methods=["GET","POST"])
def signup():

    if request.method=="POST":
        u=request.form["username"]
        p=hashlib.sha256(request.form["password"].encode()).hexdigest()

        try:
            con=db()
            con.execute("INSERT INTO users(username,password) VALUES(?,?)",(u,p))
            con.commit()
            con.close()
            return redirect("/login")
        except Exception as e:
            return str(e)

    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():

    if request.method=="POST":
        u=request.form["username"]
        p=hashlib.sha256(request.form["password"].encode()).hexdigest()

        con=db()
        cur=con.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p))
        row=cur.fetchone()
        con.close()

        if row:
            session["user"]=u
            return redirect("/")

        return "Invalid login"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/scan",methods=["POST"])
def scan():

    code=request.json["code"].lower()
    s,c,h,m,l,issues=analyze(code)

    con=db()
    con.execute("""INSERT INTO scans(user,score,critical,high,medium,low,issues,time)
    VALUES(?,?,?,?,?,?,?,?)""",
    (session["user"],s,c,h,m,l,",".join(issues),datetime.now()))
    con.commit()
    con.close()

    return jsonify({"score":s,"critical":c,"high":h,"medium":m,"low":l,"issues":issues})

if __name__=="__main__":
    app.run(debug=True)
