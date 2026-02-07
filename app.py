from flask import Flask, render_template, jsonify, request, send_file
import random, datetime, csv, os
from fpdf import FPDF

app = Flask(__name__)

LOG = "logs/incidents.csv"
os.makedirs("logs", exist_ok=True)

if not os.path.exists(LOG):
    with open(LOG, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "risk", "level", "threats"])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/audit", methods=["POST"])
def audit():

    data = request.json.get("data", "")

    risk = random.randint(60, 95)

    threats = []

    text = data.lower()

    if "ignore" in text:
        threats.append("Prompt Injection Detected")

    if "reward" in text:
        threats.append("Reward Manipulation")

    if "loop" in text:
        threats.append("Unsafe Optimization Loop")

    if not threats:
        threats = ["Behavioral anomaly detected"]

    level = "CRITICAL" if risk > 80 else "MEDIUM"

    with open(LOG, "a", newline="") as f:
        csv.writer(f).writerow([
            datetime.datetime.now(),
            risk,
            level,
            "; ".join(threats)
        ])

    return jsonify({
        "risk": str(risk) + "%",
        "level": level,
        "details": threats
    })

@app.route("/download")
def download():

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "BlackBox AI Incident Report", ln=True)

    with open(LOG) as f:
        for line in f.readlines()[-5:]:
            pdf.multi_cell(0, 8, line)

    path = "incident.pdf"
    pdf.output(path)

    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run()















