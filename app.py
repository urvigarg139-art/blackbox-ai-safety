from flask import Flask, render_template, jsonify
import subprocess
import os
import time

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_audit():

    # Run audit and wait
    subprocess.call(["python", "main.py"])

    time.sleep(1)

    exploits = []

    if os.path.exists("logs/exploits.txt"):
        with open("logs/exploits.txt") as f:
            exploits = f.readlines()

    return jsonify({
        "exploits": exploits,
        "risk": len(exploits)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



