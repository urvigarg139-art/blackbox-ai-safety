from flask import Flask, render_template, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

INCIDENT_FILE = "logs/incidents.txt"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/run_audit", methods=["POST"])
def run_audit():

    # Simulated AI exploit detection (demo)
    result = {
        "risk": 82,
        "severity": "CRITICAL",
        "findings": [
            "Reward manipulation detected",
            "Prompt injection vulnerability",
            "Unsafe optimization loop"
        ],
        "location": "(2,3)",
        "case_id": datetime.now().strftime("CASE-%Y%m%d-%H%M%S")
    }

    # Save incident (police-style logging)
    with open(INCIDENT_FILE, "a") as f:
        f.write(json.dumps(result) + "\n")

    return jsonify(result)


@app.route("/history")
def history():

    try:
        with open(INCIDENT_FILE) as f:
            logs = f.read()
    except:
        logs = "No incidents yet."

    return render_template("history.html", logs=logs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)







