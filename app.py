from flask import Flask, render_template, jsonify, request, send_file
import random, datetime, csv, os, uuid
from fpdf import FPDF

# matplotlib for server (headless)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__, static_folder="static")

LOG = "logs/incidents.csv"
os.makedirs("logs", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Create CSV if not exists
if not os.path.exists(LOG):
    with open(LOG, "w", newline="") as f:
        csv.writer(f).writerow(["case", "time", "risk", "level", "threats"])

@app.route("/")
def home():
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
    risks = []
    with open(LOG) as f:
        reader = csv.reader(f)
        next(reader)
        for r in reader:
            try:
                risks.append(int(r[2]))
            except:
                pass

    plt.clf()
    if risks:
        plt.plot(risks)
        plt.title("Risk Trend Over Time")
        plt.xlabel("Audit Count")
        plt.ylabel("Risk Score")
    else:
        plt.text(0.5, 0.5, "No data yet", ha="center")

    img_path = "static/risk.png"
    plt.savefig(img_path)
    return send_file(img_path, mimetype="image/png")

if __name__ == "__main__":
    app.run()

















