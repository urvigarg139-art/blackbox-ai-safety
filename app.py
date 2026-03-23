from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ----------- SIMPLE ANALYSIS LOGIC -----------
def analyze_code(code):
    if "SELECT" in code and "+" in code:
        return {
            "label": "⚠️ Vulnerable (SQL Injection)",
            "risk": 80,
            "confidence": 90
        }
    else:
        return {
            "label": "✅ Safe",
            "risk": 10,
            "confidence": 85
        }

# ----------- ROUTES -----------

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    code = data.get("code", "")

    result = analyze_code(code)
    return jsonify(result)

# ----------- RUN -----------

if __name__ == "__main__":
    app.run(debug=True)