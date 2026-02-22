from flask import Flask, render_template, request, jsonify, send_file
from fpdf import FPDF

app = Flask(__name__)

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
        threats.append("SQL Injection Vulnerability")

    # XSS
    if "<script>" in code:
        threats.append("Cross Site Scripting (XSS)")

    # Hardcoded secrets
    if "password" in code or "apikey" in code:
        threats.append("Hardcoded Credentials")

    # Unsafe eval
    if "eval(" in code:
        threats.append("Unsafe eval() usage")

    score = min(len(threats) * 35, 100)

    return jsonify({
        "confidence": score,
        "issues": threats
    })

@app.route("/download")
def download():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200,10,"BlackBox AI Security Report",ln=True)
    pdf.output("report.pdf")
    return send_file("report.pdf",as_attachment=True)

if __name__=="__main__":
    app.run(debug=True)



