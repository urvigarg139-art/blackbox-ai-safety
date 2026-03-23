from flask import Flask, render_template, request, jsonify, redirect, session, send_file
import sqlite3
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()


# ---------- ANALYSIS ----------
def analyze_code(code):
    if "SELECT" in code and "+" in code:
        return {
            "label": "⚠️ SQL Injection Risk",
            "risk": 82,
            "confidence": 91,
            "fix": "Use parameterized queries"
        }
    return {
        "label": "✅ Safe",
        "risk": 10,
        "confidence": 90,
        "fix": "No major issues"
    }


# ---------- ROUTES ----------
@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    
    return render_template("dashboard.html", username=session["user"])


# ---------- AUTH ----------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.form
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "⚠️ Username already exists!"

    conn.close()
    return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    data = request.form
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, password))
    user = c.fetchone()

    conn.close()

    if user:
        session["user"] = username
        return redirect("/dashboard")

    return "❌ Invalid credentials"


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# ---------- SCAN ----------
@app.route("/scan", methods=["POST"])
def scan():
    code = request.json.get("code", "")
    result = analyze_code(code)

    return jsonify(result)


# ---------- DOWNLOAD ----------
@app.route("/download", methods=["POST"])
def download():
    data = request.json

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = [
        Paragraph("AI Security Report", styles["Title"]),
        Paragraph(f"Status: {data['label']}", styles["Normal"]),
        Paragraph(f"Risk: {data['risk']}%", styles["Normal"]),
        Paragraph(f"Confidence: {data['confidence']}%", styles["Normal"]),
        Paragraph(f"Fix: {data['fix']}", styles["Normal"]),
    ]

    doc.build(content)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="report.pdf")


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)