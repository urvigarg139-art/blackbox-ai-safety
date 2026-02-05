from flask import Flask, render_template, jsonify
import subprocess
import datetime
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_audit():

    # Run your AI audit
    subprocess.Popen(["python", "main.py"])

    exploits = []

    if os.path.exists("logs/exploits.txt"):
        with open("logs/exploits.txt") as f:
            exploits = f.readlines()

    risk = len(exploits)

    return jsonify({
        "status": "Audit Running",
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "risk": risk,
        "exploits": exploits
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


