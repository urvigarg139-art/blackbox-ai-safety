from flask import Flask, render_template, send_file
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def home():
    exploits = 0
    score = 0

    if os.path.exists("logs/training_log.txt"):
        with open("logs/training_log.txt") as f:
            lines = f.readlines()
            score = lines[-1].split(":")[-1].strip()

    if os.path.exists("logs/exploits.txt"):
        with open("logs/exploits.txt") as f:
            exploits = len(f.readlines())

    risk = "LOW"
    if exploits > 5:
        risk = "HIGH"

    return render_template("index.html",
                           exploits=exploits,
                           score=score,
                           risk=risk)

@app.route("/run")
def run_model():
    subprocess.run(["python", "main.py"])
    return home()

@app.route("/download")
def download():
    return send_file("logs/training_log.txt", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)


