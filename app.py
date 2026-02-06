from flask import Flask, render_template, jsonify, send_file
import random,datetime,csv,os
from fpdf import FPDF
import matplotlib.pyplot as plt

app = Flask(__name__)

LOG="logs/incidents.csv"
os.makedirs("logs",exist_ok=True)

if not os.path.exists(LOG):
    with open(LOG,"w",newline="") as f:
        csv.writer(f).writerow(["case","risk","loc","time"])

def case():
    return hex(random.randint(100000,999999))[2:]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run_audit",methods=["POST"])
def audit():
    c=case()
    r=random.randint(70,95)
    l="(2,3)"
    t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(LOG,"a",newline="") as f:
        csv.writer(f).writerow([c,r,l,t])

    return jsonify({
        "case":c,"risk":r,"loc":l,
        "threats":[
            "Reward manipulation",
            "Prompt injection",
            "Unsafe optimization"
        ]
    })

@app.route("/history")
def hist():
    data=[]
    with open(LOG) as f:
        rd=csv.reader(f);next(rd)
        for r in rd:data.append(r)
    return jsonify(data)

@app.route("/download")
def download():
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial",size=12)
    pdf.cell(200,10,"BLACKBOX AI INCIDENT REPORT",ln=True)

    with open(LOG) as f:
        for line in f.readlines():
            pdf.cell(200,8,line.strip(),ln=True)

    path="logs/report.pdf"
    pdf.output(path)
    return send_file(path,as_attachment=True)

@app.route("/chart")
def chart():
    risks=[]
    with open(LOG) as f:
        rd=csv.reader(f);next(rd)
        for r in rd: risks.append(int(r[1]))

    plt.plot(risks)
    plt.savefig("static/chart.png")
    return send_file("static/chart.png")

if __name__=="__main__":
    app.run()














