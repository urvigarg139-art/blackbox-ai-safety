from flask import Flask, render_template, redirect, request
import subprocess
import os
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "logs/training_log.txt"
EXPLOIT_FILE = "logs/exploits.txt"


@app.route("/", methods=["GET"])
def home():
    exploits = []
    scores = []

    if os.path.exists(EXPLOIT_FILE):
        with open(EXPLOIT_FILE) as f:
            exploits = f.readlines()

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            scores = f.readlines()

    return render_template(
        "index.html",
        exploits=exploits,
        scores=scores
    )


# ✅ IMPORTANT FIX: allow POST
@app.route("/run", methods=["POST"])
def run_audit():

    # Clear previous logs
    open(LOG_FILE, "w").close()
    open(EXPLOIT_FILE, "w").close()

    # Run AI safety audit
    subprocess.call(["python", "main.py"])

    return redirect("/")


@app.route("/health")
def health():
    return {
        "status": "online",
        "timestamp": str(datetime.now())
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

