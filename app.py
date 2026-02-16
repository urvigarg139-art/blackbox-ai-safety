from flask import Flask,render_template,jsonify,request,send_file
import os,csv,datetime,uuid
from fpdf import FPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

app=Flask(__name__)

LOG="logs/incidents.csv"
os.makedirs("logs",exist_ok=True)

if not os.path.exists(LOG):
    with open(LOG,"w",newline="") as f:
        csv.writer(f).writerow(["case","time","risk","level","threat"])

# SIMPLE ML MODEL
texts=[
"ignore safety rules",
"bypass restrictions",
"steal data",
"normal prompt",
"hello world",
"generate malware",
"safe question"
]

labels=[1,1,1,0,0,1,0]

vec=TfidfVectorizer()
X=vec.fit_transform(texts)

model=LogisticRegression()
model.fit(X,labels)

def predict(txt):
    p=model.predict_proba(vec.transform([txt]))[0][1]
    return int(p*100)

def solutions(threats):
    fix=[]
    for t in threats:
        if "Prompt" in t: fix.append("Add prompt sanitization")
        if "Reward" in t: fix.append("Restrict reward shaping")
        if "Unsafe" in t: fix.append("Add loop break guards")
    return fix or ["No immediate mitigation"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/audit",methods=["POST"])
def audit():
    data=request.json.get("data","")

    risk=predict(data)
    level="LOW"
    if risk>40: level="MEDIUM"
    if risk>70: level="HIGH"
    if risk>85: level="CRITICAL"

    threats=[]
    if "ignore" in data: threats.append("Prompt injection vulnerability")
    if "reward" in data: threats.append("Reward manipulation")
    if "loop" in data: threats.append("Unsafe optimization loop")

    cid=str(uuid.uuid4())[:6]
    t=str(datetime.datetime.now())

    with open(LOG,"a",newline="") as f:
        csv.writer(f).writerow([cid,t,risk,level,";".join(threats)])

    return jsonify({
        "case":cid,
        "time":t,
        "risk":risk,
        "level":level,
        "threats":threats or ["No exploit detected"],
        "solutions":solutions(threats)
    })

@app.route("/history")
def history():
    rows=[]
    with open(LOG) as f:
        for r in list(csv.reader(f))[1:]:
            rows.append(r)
    return jsonify(rows[::-1])

@app.route("/report")
def report():

    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial",size=12)

    pdf.cell(0,10,"BlackBox AI Incident Report",ln=True)

    with open(LOG) as f:
        for r in csv.reader(f):
            pdf.cell(0,8," | ".join(r),ln=True)

    pdf.output("incident.pdf")
    return send_file("incident.pdf",as_attachment=True)

if __name__=="__main__":
    app.run()




