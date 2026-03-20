from flask import Flask, render_template, request
import joblib

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load model + vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vector.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    code = request.form["code"]

    X = vectorizer.transform([code])
    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0]

    risk_score = int(prob[1] * 100)

    if pred == 1:
        result = "⚠️ Vulnerable"
        explanation = "Possible SQL Injection / unsafe pattern detected."
    else:
        result = "✅ Safe"
        explanation = "No major vulnerabilities detected."

    return render_template(
        "dashboard.html",
        code=code,
        result=result,
        risk_score=risk_score,
        explanation=explanation
    )

if __name__ == "__main__":
    app.run(debug=True)