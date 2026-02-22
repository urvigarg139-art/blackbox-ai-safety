from flask import Flask, render_template, request, jsonify, send_file, redirect
from fpdf import FPDF
import pickle

app = Flask(__name__)

# Load ML model if available
try:
    model = pickle.load(open("model.pkl", "rb"))
except:
    model = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/audit", methods=["POST"])
def audit():

    code = request.json["data"].lower()

    threats = []
    fixes = []

    # SQL Injection
    if "select" in code and "+" in code:
        threats.append("Possible SQL Injection")
        fixes.append("Use parameterized queries instead of string concatenation.")

    # XSS
    if "<script>" in code:
        threats.append("Cross Site Scripting (XSS)")
        fixes.append("Escape HTML input and use safe rendering.")

    # Hardcoded credentials
    if "password" in code or "apikey" in code:
        threats.append("Hardcoded Credentials Detected")
        fixes.append("Store secrets in environment variables.")

    # Dangerous eval
    if "eval(" in code:
        threats.append("Unsafe eval() usage")
        fixes.append("Avoid eval(). Use safer parsing methods.")

    if len(threats) == 0:
        level = "LOW RISK"
    else:
        level = "HIGH RISK"

    return jsonify({
        "result": level,
        "issues": threats,
        "fixes": fixes
    })


@app.route("/download")
def download():

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "BlackBox AI Security Report", ln=True)
    pdf.cell(200, 10, "Threat Analysis Completed", ln=True)

    pdf.output("report.pdf")

    return send_file("report.pdf", as_attachment=True)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/login", methods=["POST"])
def login():

    u = request.form["user"]
    p = request.form["pass"]

    if u == "admin" and p == "123":
        return redirect("/dashboard")

    return "Invalid credentials"


if __name__ == "__main__":
    app.run(debug=True)




