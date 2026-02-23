from flask import Flask, render_template, request, jsonify, redirect, session
import sqlite3, hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key="blackbox_v6"

DB="blackbox.db"

def db():
    return sqlite3.connect(DB,check_same_thread=False)

def init():
    c=db()
    c.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS scans(
    id INTEGER PRIMARY KEY,
    user TEXT,
    score INTEGER,
    critical INTEGER,
    high INTEGER,
    medium INTEGER,
    low INTEGER,
    issues TEXT,
    time TEXT)""")
    c.commit();c.close()

init()

# ---------------- AI ENGINE ----------------

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

    score=min(critical*40 + high*25 + medium*20 + low*10,100)

    return score,critical,high,medium,low,issues

# ---------------- AUTH ----------------

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
            db().execute("INSERT INTO users VALUES(NULL,?,?)",(u,p))
            db().commit()
            return redirect("/login")
        except:
            return "User exists"
    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form["username"]
        p=hashlib.sha256(request.form["password"].encode()).hexdigest()
        cur=db().execute("SELECT * FROM users WHERE username=? AND password=?",(u,p))
        if cur.fetchone():
            session["user"]=u
            return redirect("/")
        return "Invalid login"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- API ----------------

@app.route("/scan",methods=["POST"])
def scan():

    code=request.json["code"].lower()
    s,c,h,m,l,issues=analyze(code)

    db().execute("INSERT INTO scans VALUES(NULL,?,?,?,?,?,?,?,?)",
    (session["user"],s,c,h,m,l,",".join(issues),datetime.now()))
    db().commit()

    return jsonify({
        "score":s,
        "critical":c,
        "high":h,
        "medium":m,
        "low":l,
        "issues":issues
    })

if __name__=="__main__":
    app.run()
