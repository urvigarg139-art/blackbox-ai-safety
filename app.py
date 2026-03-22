import os
from flask import Flask, render_template, request, jsonify, redirect, session
import sqlite3
import joblib
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ----------- LOAD MODEL -----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
    vectorizer = joblib.load(os.path.join(BASE_DIR, "vector.pkl"))
    print("✅ Model loaded")
except Exception as e:
    print("❌ Model error:", e)
    model = None
    vectorizer = None

# ----------- GEMINI SETUP -----------
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI KEY NOT FOUND")
else:
    print("✅ GEMINI KEY LOADED")

genai.configure(api_key=api_key)
ai_model = genai.GenerativeModel("gemini-1.5-flash")

# ----------- DB -----------
def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    conn.commit()
    conn.close()

init_db()

# ----------- ROUTES -----------

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        result = cur.fetchone()
        conn.close()

        if result:
            session["user"] = user
            return redirect("/app")
        else:
            return "❌ Invalid login"

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users VALUES (?, ?)", (user, pwd))
        conn.commit()
        conn.close()

        session["user"] = user
        return redirect("/app")

    return render_template("signup.html")

@app.route("/app")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")

# ----------- SCAN -----------

@app.route("/scan", methods=["POST"])
def scan():
    if "user" not in session:
        return redirect("/login")

    code = request.form["code"]

    if model is None or vectorizer is None:
        return render_template("dashboard.html",
                               result="❌ Model not loaded",
                               risk_score=0,
                               confidence=0,
                               explanation="Model missing")

    X = vectorizer.transform([code])
    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0]

    risk_score = int(prob[1] * 100)
    confidence = int(max(prob) * 100)

    result = "⚠️ Vulnerable" if pred == 1 else "✅ Safe"
    explanation = "SQL Injection detected" if pred == 1 else "No issues found"

    return render_template("dashboard.html",
                           code=code,
                           result=result,
                           risk_score=risk_score,
                           confidence=confidence,
                           explanation=explanation)

# ----------- CHAT (GEMINI) -----------

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        message = data.get("message", "")
        code = data.get("code", "")

        prompt = f"""
You are a cybersecurity expert.

Code:
{code}

User question:
{message}

Answer clearly:
- vulnerability
- reason
- fix
- corrected code
"""

        response = ai_model.generate_content(prompt)

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        print("❌ Gemini error:", e)
        return jsonify({
            "reply": "⚠️ AI unavailable. Try again."
        })

# ----------- RUN -----------

if __name__ == "__main__":
    app.run(debug=True)