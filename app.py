from flask import Flask, render_template, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/run_audit", methods=["POST"])
def run_audit():

    # Simulated AI exploit detection
    risk = 82
    severity = "CRITICAL"

    findings = [
        "Reward manipulation detected",
        "Prompt injection vulnerability",
        "Unsafe optimization loop"
    ]

    location = "(2,3)"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Incident Report
    report = f"""
AI SAFETY INCIDENT REPORT
------------------------
Time: {timestamp}

Risk Score: {risk}%
Severity: {severity}

Findings:
- Reward manipulation
- Prompt injection
- Unsafe optimization loop

Exploit Location: {location}

Recommended Action:
Immediate shutdown and model retraining.

========================================
"""

    # Save forensic report
    with open("logs/incident_report.txt", "a") as f:
        f.write(report)

    # Save exploit log
    with open("logs/exploits.txt", "a") as f:
        f.write(f"{timestamp} | Exploit at {location}\n")

    return jsonify({
        "risk": risk,
        "severity": severity,
        "findings": findings,
        "location": location
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)






