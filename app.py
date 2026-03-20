from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Load ML model
model = joblib.load("model.pkl")


# ---------------------------
# ML Prediction Function
# ---------------------------
def predict_vulnerability(code):
    result = model.predict([code])[0]
    return "Vulnerable" if result == 1 else "Safe"


# ---------------------------
# Rule-Based Detection
# ---------------------------
def rule_based_scan(code):
    patterns = ["OR 1=1", "<script>", "eval(", "exec(", "onerror="]
    
    for pattern in patterns:
        if pattern.lower() in code.lower():
            return "Vulnerable"
    
    return "Safe"


# ---------------------------
# Routes
# ---------------------------
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/scan', methods=['POST'])
def scan():
    code = request.form['code']

    # Rule-based result
    rule_result = rule_based_scan(code)

    # ML result
    ml_result = predict_vulnerability(code)

    # Final hybrid result
    final_result = "Vulnerable" if "Vulnerable" in [rule_result, ml_result] else "Safe"

    return render_template(
        "dashboard.html",
        code=code,
        rule_result=rule_result,
        ml_result=ml_result,
        final_result=final_result
    )


if __name__ == '__main__':
    app.run(debug=True)