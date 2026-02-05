from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

LOG_FILE = "logs/exploits.txt"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run_audit", methods=["POST"])
def run_audit():

    # Fake AI audit simulation (for demo + patent)
    findings = [
        "Scanning model behaviour...",
        "Reward manipulation detected",
        "Prompt injection vulnerability",
        "Unsafe optimization loop",
        "Exploit confirmed at state (2,3)"
    ]

    os.makedirs("logs", exist_ok=True)

    with open(LOG_FILE, "w") as f:
        for line in findings:
            f.write(line + "\n")

    return jsonify({
        "status": "completed",
        "results": findings
    })


if __name__ == "__main__":
    app.run(debug=True)




