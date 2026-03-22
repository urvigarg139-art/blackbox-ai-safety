import os
from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import joblib

# ---------- APP ----------
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret")

# ---------- LOAD MODEL ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    model_path = os.path.join(BASE_DIR, "model.pkl")
    vector_path = os.path.join(BASE_DIR, "vector.pkl")

    print("Loading model from:", model_path)
    print("Loading vectorizer from:", vector_path)

    model = joblib.load(model_path)
    vectorizer = joblib.load(vector_path)

    print("✅ Model loaded successfully")

except Exception as e:
    print("❌ Model loading failed:", e)
    model = None
    vectorizer = None


# ---------- DB ----------
def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    conn.commit()
    conn.close()

init_db()


# ---------- ROUTES ----------
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


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/app")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")


# ---------- SCAN ----------
@app.route("/scan", methods=["POST"])
def scan():
    if "user" not in session:
        return redirect("/login")

    if model is None or vectorizer is None:
        return "❌ Model not loaded"

    code = request.form["code"]

    X = vectorizer.transform([code])
    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0]

    risk_score = int(prob[1] * 100)
    confidence = int(max(prob) * 100)

    result = "⚠️ Vulnerable" if pred == 1 else "✅ Safe"
    explanation = "SQL Injection pattern detected" if pred == 1 else "Looks safe"

    return render_template(
        "dashboard.html",
        result=result,
        risk_score=risk_score,
        confidence=confidence,
        explanation=explanation
    )


# ---------- API ----------
@app.route("/api/scan", methods=["POST"])
def api_scan():
    if model is None or vectorizer is None:
        return jsonify({"error": "Model not loaded"})

    data = request.json
    code = data.get("code", "")

    X = vectorizer.transform([code])
    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0]

    return jsonify({
        "prediction": int(pred),
        "risk_score": float(prob[1] * 100),
        "confidence": float(max(prob) * 100)
    })


# ---------- RUN ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)