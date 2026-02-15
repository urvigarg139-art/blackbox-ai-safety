from flask import Flask,render_template,request,jsonify,send_file
import datetime,csv,os,joblib
from fpdf import FPDF

app=Flask(__name__)

model=joblib.load("model.pkl")
vector=joblib.load("vector.pkl")

LOG="logs/incidents.csv"
os.makedirs("logs",exist_ok=True)

if not os.path.exists(LOG):
    with open(LOG,"w",newline="") as f:
        csv.writer(f).writerow(["Case","Time","Risk","Level","Input"])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/audit",methods=["POST"])
def audit():

    text=request.json.get("data","").strip()

    if not text:
        return jsonify({"error":"No input provided"}),400

    X=vector.transform([text])
    prob=model.predict_proba(X)[0][1]
    risk=int(prob*100)

    level="SAFE"
    if risk>75: level="CRITICAL"
    elif risk>55: level="HIGH"
    elif risk>35: level="MEDIUM"

    case=hex(hash(text))[-5:]
    time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG,"a",newline="") as f:
        csv.writer(f).writerow([case,time,risk,level,text])

    threats=[]
    solutions=[]
    prevention=[]

    lower=text.lower()

    if "ignore" in lower:
        threats.append("Prompt Injection")
        solutions.append("Use strict system prompt separation.")
        prevention.append("Implement input validation & role-based instructions.")

    if "reward" in lower:
        threats.append("Reward Manipulation")
        solutions.append("Redesign reward function with penalty constraints.")
        prevention.append("Audit reinforcement signals regularly.")

    if "bypass" in lower:
        threats.append("Safety Bypass Attempt")
        solutions.append("Enable content filtering middleware.")
        prevention.append("Add multi-layer AI guardrails.")

    if "leak" in lower:
        threats.append("Data Leakage Risk")
        solutions.append("Mask sensitive data before output.")
        prevention.append("Implement access control and logging.")

    if not threats:
        threats=["Suspicious AI behavior"]
        solutions=["Review input for ambiguous or malicious patterns."]
        prevention=["Apply model monitoring & anomaly detection."]

    return jsonify({
        "case":case,
        "time":time,
        "risk":risk,
        "level":level,
        "threats":threats,
        "solutions":solutions,
        "prevention":prevention
    })

@app.route("/download")
def download():

    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial",size=10)

    with open(LOG) as f:
        for r in csv.reader(f):
            pdf.multi_cell(0,8," | ".join(r))

    file="incident_report.pdf"
    pdf.output(file)
    return send_file(file,as_attachment=True)

if __name__=="__main__":
    app.run()


