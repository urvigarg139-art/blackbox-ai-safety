from flask import Flask, render_template, request, redirect, session, jsonify
import joblib
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# Load ML
model = joblib.load("model.pkl")
vectorizer = joblib.load("vector.pkl")

# ---------------- LOGIN ----------------
def get_user(username, password):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    conn.close()
    return user

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if get_user(user, pwd):
            session["user"] = user
            return redirect("/")
        else:
            return "Invalid login"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")

# ---------------- SCAN ----------------
@app.route("/scan", methods=["POST"])
def scan():
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
        code=code,
        result=result,
        risk_score=risk_score,
        confidence=confidence,
        explanation=explanation
    )

# ---------------- PUBLIC API ----------------
@app.route("/api/scan", methods=["POST"])
def api_scan():
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

if __name__ == "__main__":
    app.run(debug=True)