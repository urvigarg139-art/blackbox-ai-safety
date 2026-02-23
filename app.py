from flask import Flask, render_template, request, jsonify, redirect, session
import sqlite3, hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "blackbox_v5"

DB="blackbox.db"

def db():
    return sqlite3.connect(DB)

# ---------- INIT ----------

with db() as con:
    con.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT)""")

    con.execute("""CREATE TABLE IF NOT EXISTS scans(
    id INTEGER PRIMARY KEY,
    user TEXT,
    score INTEGER,
    issues TEXT,
    category TEXT,
    time TEXT)""")

# ---------- ML STYLE SCORER ----------

def ai_score(code):

    score=0
    issues=[]
    category=[]

    if "select" in code and "+" in code:
        score+=25
        issues.append("SQL Injection")
        category.append("Injection")

    if "<script>" in code:
        score+=25
        issues.append("XSS")
        category.append("Client Side")

    if "password" in code:
        score+=25
        issues.append("Hardcoded Secret")
        category.append("Credential Leak")

    if "eval(" in code:
        score+=25
        issues.append("Unsafe Eval")
        category.append("Code Execution")

    return min(score,100),issues,category

# ---------- AUTH ----------

@app.route("/",methods=["GET"])
def home():
    if "user" not in session:
        return redirect("/login")

    with db() as con:
        rows=con.execute("SELECT score FROM scans WHERE user=?",(session["user"],)).fetchall()

    avg=int(sum([r[0] for r in rows])/len(rows)) if rows else 0
    return render_template("index.html",user=session["user"],avg=avg)

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        u=request.form["username"]
        p=hashlib.sha256(request.form["password"].encode()).hexdigest()

        try:
            with db() as con:
                con.execute("INSERT INTO users VALUES(NULL,?,?)",(u,p))
            return redirect("/login")
        except:
            return "User exists"

    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form["username"]
        p=hashlib.sha256(request.form["password"].encode()).hexdigest()

        with db() as con:
            cur=con.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p))
            if cur.fetchone():
                session["user"]=u
                return redirect("/")

        return "Invalid login"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------- API ----------

@app.route("/scan",methods=["POST"])
def scan():

    code=request.json["code"].lower()
    score,issues,category=ai_score(code)

    with db() as con:
        con.execute("INSERT INTO scans VALUES(NULL,?,?,?,?,?)",
        (session["user"],score,",".join(issues),",".join(category),datetime.now()))

    return jsonify({
        "score":score,
        "issues":issues,
        "category":category
    })

@app.route("/history")
def history():
    with db() as con:
        rows=con.execute("SELECT score,time FROM scans WHERE user=?",(session["user"],)).fetchall()
    return jsonify(rows)

if __name__=="__main__":
    app.run(debug=True)
