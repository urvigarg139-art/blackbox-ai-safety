from flask import Flask, render_template, request, jsonify, send_file
import random, datetime, csv, os
from fpdf import FPDF

app = Flask(__name__)

LOG = "logs/incidents.csv"
os.makedirs("logs", exist_ok=True)

if not os.path.exists(LOG):
    with open(LOG, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["CaseID","Time","Risk","Level","Threats"])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/audit", methods=["POST"])
def audit():
    data = request.json.get("data","")

    threats = [
        "Reward manipulation detected",
        "Prompt injection vulnerability",
        "Unsafe optimization loop"
    ]

    risk = random.randint(70,90)
    level = "CRITICAL" if risk>80 else "HIGH"
    case = hex(random.randint(100000,999999))[2:]
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG,"a",newline="") as f:
        csv.writer(f).writerow([case,t,risk,level," | ".join(threats)])

    return jsonify({
        "case":case,
        "time":t,
        "risk":risk,
        "level":level,
        "threats":threats
    })

@app.route("/download")
def download():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial",size=12)

    pdf.cell(0,10,"BLACKBOX AI INCIDENT REPORT",ln=True)

    with open(LOG) as f:
        rows=list(csv.reader(f))[1:]

    for r in rows[-1:]:
        pdf.multi_cell(0,8,f"""
Case ID: {r[0]}
Time: {r[1]}
Risk Score: {r[2]}%
Threat Level: {r[3]}
Findings:
{r[4]}
""")

    path="incident.pdf"
    pdf.output(path)

    return send_file(path,as_attachment=True)

if __name__=="__main__":
    app.run(debug=True)




















