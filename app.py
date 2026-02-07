from flask import Flask, render_template, jsonify, send_file
import random, datetime, csv, os
from fpdf import FPDF

app = Flask(__name__)

LOG = "logs/incidents.csv"
os.makedirs("logs", exist_ok=True)

if not os.path.exists(LOG):
    with open(LOG, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "case_id", "risk", "location", "threats"])


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/audit")
def audit():

    threats = [
        "Reward manipulation detected",
        "Prompt injection vulnerability",
        "Unsafe optimization loop"
    ]

    score = random.randint(70, 95)
    case = hex(random.randint(100000, 999999))[2:]
    location = "(2,3)"

    with open(LOG, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.datetime.now(),
            case,
            score,
            location,
            ";".join(threats)
        ])

    return jsonify({
        "case": case,
        "risk": score,
        "location": location,
        "threats": threats
    })


@app.route("/report")
def report():

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "BlackBox AI Incident Report", ln=True)

    with open(LOG) as f:
        reader = csv.reader(f)
        for row in reader:
            pdf.multi_cell(0, 8, " | ".join(row))

    path = "incident_report.pdf"
    pdf.output(path)

    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run()















