from flask import Flask, render_template, request, jsonify, send_file, redirect
from fpdf import FPDF
import pickle

app = Flask(__name__)

# Load model (optional if you use real ML later)
try:
    model = pickle.load(open("model.pkl", "rb"))
except:
    model = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/audit", methods=["POST"])
def audit():
    data = request.json["data"]

    if len(data) > 100:
        result = "HIGH RISK"
    else:
        result = "LOW RISK"

    return jsonify({"result": result})

@app.route("/download")
def download():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "BlackBox AI Security Report", ln=True)
    pdf.cell(200, 10, "Threat Analysis Complete", ln=True)

    pdf.output("report.pdf")
    return send_file("report.pdf", as_attachment=True)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/login", methods=["POST"])
def login():
    u = request.form["user"]
    p = request.form["pass"]

    if u == "admin" and p == "123":
        return redirect("/dashboard")

    return "Invalid credentials"

if __name__ == "__main__":
    app.run(debug=True)




