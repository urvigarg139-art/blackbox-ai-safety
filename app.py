from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = "blackbox_secret_key"

users = {
    "admin": "123",
    "urvi": "pass"
}

user_history = {}

@app.route("/")
def home():
    if "user" in session:
        history = user_history.get(session["user"], [])
        total = len(history)
        avg = int(sum([s["score"] for s in history]) / total) if total > 0 else 0
        return render_template("index.html", user=session["user"], total=total, avg=avg)
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["user"] = username
            if username not in user_history:
                user_history[username] = []
            return redirect(url_for("home"))
        error = "Invalid username or password"

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/audit", methods=["POST"])
def audit():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    code = request.json["data"].lower()
    threats = []

    if "select" in code and "+" in code:
        threats.append("SQL Injection Vulnerability")

    if "<script>" in code:
        threats.append("Cross Site Scripting (XSS)")

    if "password" in code:
        threats.append("Hardcoded Credentials")

    if "eval(" in code:
        threats.append("Unsafe eval() usage")

    score = min(len(threats) * 35, 100)
    scan = {"score": score, "issues": threats}
    user_history[session["user"]].append(scan)

    return jsonify(scan)

@app.route("/history")
def history():
    return jsonify(user_history.get(session["user"], []))

@app.route("/clear")
def clear():
    user_history[session["user"]] = []
    return redirect(url_for("home"))

@app.route("/download")
def download():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "BlackBox AI Security Report", ln=True)
    pdf.output("report.pdf")
    return send_file("report.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)


