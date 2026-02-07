from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for
import random, datetime, csv, os, uuid
from fpdf import FPDF

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__, static_folder="static")
app.secret_key = "blackbox-secret"

LOG = "logs/incidents.csv"
os.makedirs("logs", exist_ok=True)
os.makedirs("static", exist_ok=True)

if not os.path.exists(LOG):
    with open(LOG, "w", newline="") as f:
        csv.writer(f).writerow(["case", "time", "risk", "level", "threats"])

# --- SIMPLE LOGIN (demo) ---
USERS = {
    "admin": "admin123",
    "operator": "operator123"
}

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")
        if USERS.get(u) == p:
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("index.html")

@app.route("/audit", methods=["POST"])
def audit():
    text = request.json.get("data", "").lower()

    threats = []
    if "ignore" in text: threats.append("Prompt Injection")
    if "reward" in text: threats.append("Reward Manipulation")
    if "loop" in text: threats.append("Unsafe Optimization")

    if not threats:
        threats.append("Behavioral anomaly")

    risk = random.randint(60, 95)
    level = "CRITICAL" if risk > 80 else "MEDIUM"

    case = str(uuid.uuid4())[:8]
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG, "a", newline="") as f:
        csv.writer(f).writerow([case, time, risk, level, ";".join(threats)])

    return jsonify({
        "case": case,
        "risk": risk,
        "level": level,
        "threats": threats,
        "time": time
    })

@app.route("/history")
def history():
    rows=[]
    with open(LOG) as f:
        rd=csv.reader(f)
        next(rd)
        for r in rd:
            rows.append(r)
    return jsonify(rows)

@app.route("/download")
def download():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "BLACKBOX AI INCIDENT REPORT", ln=True)

    with open(LOG) as f:
        for line in f.readlines()[-10:]:
            pdf.multi_cell(0, 8, line.strip())

    path = "incident.pdf"
    pdf.output(path)
    return send_file(path, as_attachment=True)

@app.route("/chart")
def chart():
    risks=[]
    with open(LOG) as f:
        rd=csv.reader(f)
        next(rd)
        for r in rd:
            try: risks.append(int(r[2]))
            except: pass

    plt.clf()
    if risks:
        plt.plot(risks)
        plt.title("Risk Trend")
    img="static/risk.png"
    plt.savefig(img)
    return send_file(img, mimetype="image/png")

if __name__ == "__main__":
    app.run()


















