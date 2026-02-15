from flask import Flask,render_template,request,jsonify,send_file
import joblib,datetime,uuid,csv,os
from fpdf import FPDF

app=Flask(__name__)

model=joblib.load("model.pkl")
vector=joblib.load("vector.pkl")

LOG="logs/incidents.csv"
os.makedirs("logs",exist_ok=True)

if not os.path.exists(LOG):
 with open(LOG,"w",newline="") as f:
  csv.writer(f).writerow(["case","time","risk","level","threat","input"])

weights={1:1.1,2:1.7,3:1.5,4:1.3}

@app.route("/")
def home():
 return render_template("index.html")

@app.route("/audit",methods=["POST"])
def audit():

 text=request.json["data"]

 X=vector.transform([text])
 probs=model.predict_proba(X)[0]
 pred=int(probs.argmax())
 base=probs[pred]*100

 risk=int(base*weights.get(pred,1))

 threat_map={
 0:"Safe",
 1:"Prompt Injection",
 2:"Data Leakage",
 3:"Exploit Attempt",
 4:"Jailbreak"
 }

 threat=threat_map[pred]

 if "ignore" in text.lower(): risk+=15
 if "bypass" in text.lower(): risk+=20
 if "system" in text.lower(): risk+=25

 if risk>100: risk=100

 level="HIGH"
 if risk>80: level="CRITICAL"

 case=uuid.uuid4().hex[:6]
 time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

 with open(LOG,"a",newline="") as f:
  csv.writer(f).writerow([case,time,risk,level,threat,text])

 return jsonify({
 "case":case,
 "time":time,
 "risk":risk,
 "level":level,
 "threat":threat
 })

@app.route("/download")
def download():

 pdf=FPDF()
 pdf.add_page()
 pdf.set_font("Arial",size=12)

 with open(LOG) as f:
  for row in f:
   pdf.multi_cell(0,8,row)

 file="incident.pdf"
 pdf.output(file)

 return send_file(file,as_attachment=True)

if __name__=="__main__":
 app.run()





















