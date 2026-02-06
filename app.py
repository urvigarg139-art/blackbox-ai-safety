from flask import Flask, render_template, jsonify, send_file
import os
import json
from datetime import datetime

app = Flask(__name__)

# Always create logs folder + file
os.makedirs("logs", exist_ok=True)

INCIDENT_FILE = "logs/incidents.txt"

if not os.path.exists(INCIDENT_FILE):
    open(INCIDENT_FILE, "w").close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/run_audit", methods=["POST"])
def run_audit():

    result = {
        "risk": 82,
        "severity": "CRITICAL",
        "findings": [
            "Reward manipulation detected",
            "Prompt injection vulnerability",
            "Unsafe optimization loop"
        ],
        "location": "(2,3)",
        "case_id": datetime.now().strftime("CASE-%Y%m%d-%H%M%S"),
        "timestamp": datetime.now().isoformat()
    }

    with open(INCIDENT_FILE, "a") as f:
        f.write(json.dumps(result) + "\n")

    return jsonify(result)


@app.route("/history")
def history():
    with open(INCIDENT_FILE) as f:
        logs = f.read()

    return f"<pre>{logs if logs else 'No incidents yet.'}</pre>"


@app.route("/download")
def download_report():

    if os.path.getsize(INCIDENT_FILE) == 0:
        return "No incidents recorded yet. Run audit first."

    return send_file(
        INCIDENT_FILE,
        as_attachment=True,
        download_name="AI_Incident_Report.txt"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)









