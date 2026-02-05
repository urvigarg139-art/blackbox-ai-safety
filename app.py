from flask import Flask, render_template, jsonify, request
import os
import subprocess
from datetime import datetime

app = Flask(__name__)

LOG_DIR = "logs"
EXPLOIT_FILE = os.path.join(LOG_DIR, "exploits.txt")

os.makedirs(LOG_DIR, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


# ✅ IMPORTANT: allow POST
@app.route("/run", methods=["POST"])
def run_audit():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Run your ML system
        subprocess.run(["python", "main.py"], check=True)

        # Read exploit file if exists
        exploits = []
        if os.path.exists(EXPLOIT_FILE):
            with open(EXPLOIT_FILE, "r") as f:
                exploits = f.readlines()

        return jsonify({
            "status": "completed",
            "time": timestamp,
            "exploits": exploits[-10:]
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

