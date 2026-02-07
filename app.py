from flask import Flask, render_template, jsonify, request, send_file
import random, datetime, csv, os
from fpdf import FPDF

app = Flask(__name__)

LOG = "logs/incidents.csv"
os.makedirs("logs", exist_ok=True)

# Create CSV if missing
if not os.path.exists(LOG):
    with open(LOG, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["case", "time", "risk"])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/audit", methods=["POST"])
def audit():

    data = request.json.get("data", "")

    threats = []

    text = data.lower()

    if "ignore" in text or "bypass" in text:
        threats.append("Prompt injection attempt")

    if "reward" in text:
        threats.append("Reward manipulation")

    if len(text) > 200:
        threats.append("Unsafe optimization loop")

    if not threats:
        threats.append("No threats detected")

    risk = random.randint(40, 90)
    level = "CRITICAL" if risk > 70 else "MEDIUM"

    case = str(random.randint(100000, 999999))
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG, "a", newline="") as f:
        csv.writer(f).writerow([case, time, risk])

    return jsonify({
        "case": case,
        "time": time,
        "risk": risk,
        "level": level,
        "threats": threats
    })

@app.route("/history")
def history():

    rows = []

    with open(LOG) as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    return jsonify(rows)

@app.route("/download")
def download():

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0,10,"BlackBox AI Incident Report", ln=True)
    pdf.ln(5)

    with open(LOG) as f:
        reader = csv.reader(f)
        for row in reader:
            pdf.cell(0,8," | ".join(row), ln=True)

    filename = "incident_report.pdf"
    pdf.output(filename)

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)



















