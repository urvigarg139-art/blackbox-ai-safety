from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run")
def run_audit():
    subprocess.Popen(["python", "main.py"])
    return "Audit started. Check logs."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
