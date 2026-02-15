from flask import Flask, render_template, request, jsonify, send_file
import random, datetime, csv, os
from fpdf import FPDF

app = Flask(__name__)

LOG_FILE = "logs/incidents.csv"
os.makedirs("logs", exist_ok=True)

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE,"w",newline="") as f:
        csv.writer(f).writerow(["case","time","risk"])

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
    level = "CRITICAL" if risk>80 else "MEDIUM"

    case = hex(random.randint(1000000,9999999))[2:]
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE,"a",newline="") as f:
        csv.writer(f).writerow([case,time,risk])

    return jsonify({
        "case":case,
        "time":time,
        "risk":risk,
        "level":level,
        "threats":threats,
        "exploit":"(2,3)"
    })

@app.route("/history")
def history():

    rows=[]
    with open(LOG_FILE) as f:
        reader=csv.DictReader(f)
        for r in reader:
            rows.append(r)

    return jsonify(rows[::-1])

@app.route("/download")
def download():

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,"BlackBox AI Threat Report",ln=1)

    pdf.set_font("Arial","",12)

    with open(LOG_FILE) as f:
        reader=csv.reader(f)
        next(reader)

        for row in reader:
            pdf.cell(0,8,f"Case: {row[0]} | Time: {row[1]} | Risk: {row[2]}%",ln=1)

    path="logs/report.pdf"
    pdf.output(path)

    return send_file(path,as_attachment=True)

if __name__=="__main__":
    app.run(debug=True)




















