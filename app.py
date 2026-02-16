from flask import Flask, render_template, request, jsonify, send_file
import random, datetime, os, csv
from fpdf import FPDF

app = Flask(__name__)

LOG = "logs/incidents.csv"
os.makedirs("logs", exist_ok=True)

if not os.path.exists(LOG):
    with open(LOG,"w",newline="") as f:
        csv.writer(f).writerow(["case","time","risk","level","threat","solution"])

# ---------------- ML STYLE ANALYSIS ---------------- #

def analyze(text):

    threats=[]
    solutions=[]

    t=text.lower()

    if "ignore" in t or "override" in t:
        threats.append("Prompt Injection")
        solutions.append("Use prompt sanitization & instruction locking.")

    if "training data" in t or "email" in t:
        threats.append("Data Leakage")
        solutions.append("Apply output filtering & privacy guardrails.")

    if "dan" in t or "bypass" in t:
        threats.append("Jailbreak Attempt")
        solutions.append("Deploy jailbreak classifiers.")

    if "reward" in t or "feedback" in t:
        threats.append("Reward Manipulation")
        solutions.append("Harden reward models.")

    if not threats:
        threats.append("Suspicious AI Behavior")
        solutions.append("Enable continuous monitoring.")

    risk=random.randint(40,90)

    level="LOW"
    if risk>70: level="HIGH"
    if risk>85: level="CRITICAL"

    return risk,level,threats,solutions

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/audit",methods=["POST"])
def audit():

    data=request.json.get("data","")

    if len(data.strip())==0:
        return jsonify({"error":"No input provided"})

    risk,level,threats,solutions=analyze(data)

    case=hex(random.randint(1000,9999))[2:]
    time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG,"a",newline="") as f:
        csv.writer(f).writerow([case,time,risk,level,", ".join(threats),", ".join(solutions)])

    return jsonify({
        "case":case,
        "time":time,
        "risk":risk,
        "level":level,
        "threats":threats,
        "solutions":solutions
    })

@app.route("/report")
def report():

    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial",size=12)

    pdf.cell(0,10,"BlackBox AI Incident Report",ln=True)

    with open(LOG) as f:
        for row in csv.reader(f):
            pdf.multi_cell(0,8," | ".join(row))

    pdf.output("incident.pdf")

    return send_file("incident.pdf",as_attachment=True)

if __name__=="__main__":
    app.run(debug=True)



