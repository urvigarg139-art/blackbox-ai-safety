from flask import Flask, render_template, request, jsonify
import random
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/audit", methods=["POST"])
def audit():
    findings = [
        "Reward manipulation detected",
        "Prompt injection vulnerability",
        "Unsafe optimization loop"
    ]

    risk_score = random.randint(70, 95)

    result = {
        "time": str(datetime.datetime.now()),
        "risk": risk_score,
        "severity": "CRITICAL" if risk_score > 80 else "HIGH",
        "findings": findings,
        "location": "(2,3)"
    }

    with open("logs/exploits.txt", "a") as f:
        f.write(str(result) + "\n")

    return jsonify(result)

if __name__ == "__main__":
    app.run()





