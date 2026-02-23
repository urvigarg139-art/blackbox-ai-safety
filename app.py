from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "blackbox_v4_secret"

DB = "blackbox.db"


def db():
    return sqlite3.connect(DB)


# ---------- INIT DATABASE ----------

with db() as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS scans(
        id INTEGER PRIMARY KEY,
        user TEXT,
        score INTEGER,
        issues TEXT,
        time TEXT)""")


# ---------- AUTH ----------

@app.route("/", methods=["GET"])
def home():
    if "user" not in session:
        return redirect("/login")

    with db() as con:
        cur = con.cursor()
        cur.execute("SELECT score FROM scans WHERE user=?", (session["user"],))
        rows = cur.fetchall()

    total = len(rows)
    avg = int(sum([r[0] for r in rows]) / total) if total else 0

    return render_template("index.html", user=session["user"], total=total, avg=avg)


@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method=="POST":
        u=request.form["username"]
        p=request.form["password"]

        try:
            with db() as con:
                con.execute("INSERT INTO users VALUES(NULL,?,?)",(u,p))
            return redirect("/login")
        except:
            return "Username already exists"

    return render_template("signup.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form["username"]
        p=request.form["password"]

        with db() as con:
            cur=con.cursor()
            cur.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p))
            if cur.fetchone():
                session["user"]=u
                return redirect("/")

        return "Invalid credentials"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------- SCANNER ----------

@app.route("/audit", methods=["POST"])
def audit():

    code=request.json["data"].lower()
    issues=[]

    if "select" in code and "+" in code:
        issues.append("SQL Injection")

    if "<script>" in code:
        issues.append("XSS")

    if "password" in code:
        issues.append("Hardcoded Secret")

    if "eval(" in code:
        issues.append("Unsafe eval")

    score=min(len(issues)*25,100)

    with db() as con:
        con.execute("INSERT INTO scans VALUES(NULL,?,?,?,?)",
        (session["user"],score,",".join(issues),datetime.now()))

    return jsonify({"score":score,"issues":issues})


@app.route("/history")
def history():
    with db() as con:
        cur=con.cursor()
        cur.execute("SELECT score,time FROM scans WHERE user=?",(session["user"],))
        return jsonify(cur.fetchall())


if __name__=="__main__":
    app.run(debug=True)

