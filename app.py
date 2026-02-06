from flask import Flask, render_template, jsonify, send_file
import random
import datetime
import csv
import os

app = Flask(__name__)

INCIDENT_FILE = "logs/incidents.csv"

os.makedirs("logs", exist_ok=True)

if not os.path.exists(INCIDENT_FILE):
    with open(INCIDENT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["case_id", "risk", "location", "time"])

def generate_case():
    return hex(random.randint(1000000,9999999))[2:]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run_audit", methods=["POST"])
def run_audit():
    case = generate_case()
    risk = random.randint(70,95)
    loc = "(2,3)"
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(INCIDENT_FILE,"a",newline="") as f:
        writer = csv.writer(f)
        writer.writerow([case,risk,loc,time])

    return jsonify({
        "case": case,
        "risk": risk,
        "location": loc,
        "threats":[
            "Reward manipulation detected",
            "Prompt injection vulnerability",
            "Unsafe optimization loop"
        ]
    })

@app.route("/history")
def history():
    rows=[]
    with open(INCIDENT_FILE) as f:
        reader=csv.reader(f)
        next(reader)
        for r in reader:
            rows.append(r)

    return jsonify(rows)

@app.route("/download")
def download():
    return send_file(INCIDENT_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run()












