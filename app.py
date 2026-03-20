from flask import Flask, render_template, request, jsonify
import joblib

app = Flask(__name__)

# Load ML model
model = joblib.load("model.pkl")


# ---------------------------
# ML Prediction
# ---------------------------
def predict_vulnerability(code):
    pred = model.predict([code])[0]
    prob = model.predict_proba([code])[0][1]
    return pred, prob


# ---------------------------
# Rule-Based Detection
# ---------------------------
def rule_based_scan(code):
    rules = {
        "SQL Injection": ["OR 1=1", "' OR '1'='1"],
        "XSS Attack": ["<script>", "onerror="],
        "Command Injection": ["os.system", "exec(", "eval("],
        "Hardcoded Secret": ["password =", "api_key ="]
    }

    detected = []

    for attack, patterns in rules.items():
        for pattern in patterns:
            if pattern.lower() in code.lower():
                detected.append(attack)

    return detected


# ---------------------------
# Risk Score
# ---------------------------
def calculate_risk(prob, rule_hits):
    base = int(prob * 100)
    bonus = len(rule_hits) * 10
    return min(base + bonus, 100)


# ---------------------------
# Routes
# ---------------------------
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/scan', methods=['POST'])
def scan():
    code = request.form['code']

    pred, prob = predict_vulnerability(code)
    ml_result = "Vulnerable" if pred == 1 else "Safe"

    rule_hits = rule_based_scan(code)
    rule_result = "Vulnerable" if rule_hits else "Safe"

    final_result = "Vulnerable" if ml_result == "Vulnerable" or rule_result == "Vulnerable" else "Safe"

    risk_score = calculate_risk(prob, rule_hits)

    return render_template(
        "dashboard.html",
        code=code,
        ml_result=ml_result,
        rule_result=rule_result,
        final_result=final_result,
        risk_score=risk_score,
        explanations=rule_hits
    )


# ---------------------------
# API (SaaS Ready)
# ---------------------------
@app.route('/api/scan', methods=['POST'])
def api_scan():
    data = request.get_json()
    code = data.get("code", "")

    pred, prob = predict_vulnerability(code)
    rule_hits = rule_based_scan(code)

    return jsonify({
        "prediction": "Vulnerable" if pred == 1 else "Safe",
        "risk_score": calculate_risk(prob, rule_hits),
        "issues": rule_hits
    })


if __name__ == '__main__':
    app.run(debug=True)