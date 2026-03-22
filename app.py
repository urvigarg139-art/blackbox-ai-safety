from flask import Flask, render_template, request, jsonify, send_file
import io
from reportlab.pdfgen import canvas

app = Flask(__name__)

# ---------- ANALYSIS ----------
def analyze_code(code):
    vulnerabilities = []
    lines = code.split("\n")
    highlighted = []

    for i, line in enumerate(lines):
        if "SELECT" in line and "user_input" in line:
            vulnerabilities.append(("SQL Injection", 80, i))
        if "<script>" in line:
            vulnerabilities.append(("XSS Attack", 70, i))
        if "os.system" in line:
            vulnerabilities.append(("Command Injection", 85, i))
        if "password =" in line:
            vulnerabilities.append(("Hardcoded Secret", 60, i))

    for i, line in enumerate(lines):
        flag = False
        for v in vulnerabilities:
            if v[2] == i:
                flag = True
        if flag:
            highlighted.append(f">>> {line}")
        else:
            highlighted.append(line)

    if vulnerabilities:
        result = "Vulnerable"
        risk = max(v[1] for v in vulnerabilities)
        confidence = 100 - risk
    else:
        result = "Safe"
        risk = 10
        confidence = 90

    return result, risk, confidence, vulnerabilities, "\n".join(highlighted)


def generate_fix(vuln):
    fixes = {
        "SQL Injection": "Use parameterized queries.",
        "XSS Attack": "Escape HTML inputs.",
        "Command Injection": "Avoid os.system().",
        "Hardcoded Secret": "Use environment variables."
    }
    return fixes.get(vuln, "Follow secure practices.")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    code = data.get("code", "")

    result, risk, confidence, vulnerabilities, highlighted = analyze_code(code)
    fixes = [generate_fix(v[0]) for v in vulnerabilities]

    return jsonify({
        "result": result,
        "risk": risk,
        "confidence": confidence,
        "code": code,
        "highlighted": highlighted,
        "vulnerabilities": vulnerabilities,
        "fixes": fixes
    })
    return jsonify({
    "label": "Vulnerable",
    "risk": 80,
    "confidence": 20,
    "reason": "User input is directly concatenated → SQL Injection risk.",
    "fix": "Use parameterized queries:\nSELECT * FROM users WHERE id = ?"
})


# ---------- PDF ----------
@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)

    text = c.beginText(40, 800)
    text.textLine("AI Security Report")
    text.textLine(f"Result: {data['result']}")
    text.textLine(f"Risk: {data['risk']}%")

    for f in data["fixes"]:
        text.textLine(f"- {f}")

    c.drawText(text)
    c.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="report.pdf")