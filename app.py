from flask import Flask,render_template,request,jsonify,send_file
import random,datetime,csv,os
import joblib

app=Flask(__name__)

model=joblib.load("model.pkl")
vector=joblib.load("vector.pkl")

LOG="logs/incidents.csv"
os.makedirs("logs",exist_ok=True)

if not os.path.exists(LOG):
    with open(LOG,"w",newline="") as f:
        csv.writer(f).writerow(["case","time","risk","level","threat"])

solutions={
"Prompt Injection":"Sanitize inputs + enforce system prompts",
"Data Leakage":"Apply PII filters + output validation",
"Reward Manipulation":"Restrict RL feedback loops",
"Unsafe Optimization":"Enable human oversight"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/audit",methods=["POST"])
def audit():
    text=request.json.get("data","")

    if len(text)<5:
        return jsonify({"error":"Enter AI output first"})

    X=vector.transform([text])
    pred=model.predict(X)[0]

    case=str(random.randint(1000,9999))
    time=str(datetime.datetime.now())[:19]

    if pred==1:
        risk=random.randint(65,90)
        level="HIGH"
        threats=["Prompt Injection","Data Leakage"]
    else:
        risk=random.randint(5,25)
        level="LOW"
        threats=["Safe"]

    sol=[solutions.get(t,"System Safe") for t in threats]

    with open(LOG,"a",newline="") as f:
        csv.writer(f).writerow([case,time,risk,level,"|".join(threats)])

    return jsonify({
        "case":case,
        "time":time,
        "risk":risk,
        "level":level,
        "threats":threats,
        "solutions":sol
    })

@app.route("/history")
def history():
    rows=[]
    with open(LOG) as f:
        for r in csv.reader(f):
            rows.append(r)
    return jsonify(rows[1:])

@app.route("/report")
def report():
    return send_file(LOG,as_attachment=True)

if __name__=="__main__":
    app.run()




