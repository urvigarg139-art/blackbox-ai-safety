from flask import Flask, render_template, request, jsonify, send_file
import random, datetime, csv, os
from fpdf import FPDF

app = Flask(__name__)

LOG = "logs/incidents.csv"
os.makedirs("logs", exist_ok=True)

if not os.path.exists(LOG):
    with open(LOG, "w", newline="") as f:
        csv.writer(f).writerow(["CaseID","Time","Risk","Level","Threats"])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/audit", methods=["POST"])
def audit():

    data = request.json.get("data","").strip()

    # 🚨 NO INPUT → STOP
    if not data:
        return jsonify({"error":"No input provided"}),400

    threats=[]

    if "ignore" in data.lower():
        threats.append("Prompt injection vulnerability")

    if "reward" in data.lower():
        threats.append("Reward manipulation detected")

    if len(data)>200:
        threats.append("Unsafe optimization loop")

    if not threats:
        threats.append("Suspicious behavior pattern")

    risk=random.randint(50,90)

    level="MEDIUM"
    if risk>80: level="CRITICAL"
    elif risk>65: level="HIGH"

    case=hex(random.randint(1000,9999))[2:]
    time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG,"a",newline="") as f:
        csv.writer(f).writerow([case,time,risk,level," | ".join(threats)])

    return jsonify({
        "case":case,
        "time":time,
        "risk":risk,
        "level":level,
        "threat":"AI Behavior Exploit",
        "threats":threats
    })

@app.route("/download")
def download():

    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial",size=12)
    pdf.cell(0,10,"BlackBox AI Incident Report",ln=True)

    with open(LOG) as f:
        for row in csv.reader(f):
            pdf.multi_cell(0,8," | ".join(row))

    file="incident_report.pdf"
    pdf.output(file)

    return send_file(file,as_attachment=True)

if __name__=="__main__":
    app.run()
