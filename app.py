from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def analyze_code(code):
    if "SELECT" in code and "+" in code:
        return {
            "label": "⚠️ Vulnerable (SQL Injection)",
            "risk": 82,
            "confidence": 91
        }
    elif "eval(" in code:
        return {
            "label": "⚠️ Dangerous (Code Injection)",
            "risk": 75,
            "confidence": 88
        }
    else:
        return {
            "label": "✅ Safe",
            "risk": 12,
            "confidence": 86
        }

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    code = data.get("code", "")
    result = analyze_code(code)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)