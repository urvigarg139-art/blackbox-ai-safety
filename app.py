from flask import Flask, render_template, request, jsonify, send_file, redirect
from fpdf import FPDF
import pickle

app = Flask(__name__)

# Optional ML model
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

    # Language detection
    if "<html" in code:
        language = "HTML"
    elif "def " in code:
        language = "Python"
    elif "function" in code:
        language = "JavaScript"
    else:
        language = "Unknown"

    # SQL Injection
    if "select" in code and "+" in code:
        threats.append("Possible SQL Injection")
        fixes.append("Use parameterized queries.")

    # XSS
    if "<script>" in code:
        threats.append("Cross Site Scripting (XSS)")
        fixes.append("Escape HTML input.")

    # Hardcoded secrets
    if "password" in code or "apikey" in code:
        threats.append("Hardcoded Credentials")
        fixes.append("Use environment variables.")

    # Unsafe eval
    if "eval(" in code:
        threats.append("Unsafe eval() usage")
        fixes.append("Avoid eval.")

    score = min(len(threats) * 25, 100)

    if score == 0:
        level = "LOW RISK"
    elif score < 50:
        level = "MEDIUM RISK"
    else:
        level = "HIGH RISK"

    return jsonify({
        "result": level,
        "issues": threats,
        "fixes": fixes,
        "confidence": score,
        "language": language
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


if __name__ == "__main__":
    app.run(debug=True)




