import os
from flask import Flask, render_template, request, jsonify
import joblib
from openai import OpenAI

app = Flask(__name__)

# ---------- LOAD MODEL ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
    vectorizer = joblib.load(os.path.join(BASE_DIR, "vector.pkl"))
    print("✅ Model loaded")
except Exception as e:
    print("❌ Model error:", e)
    model = None
    vectorizer = None

# ---------- OPENAI ----------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- CHAT + ML ----------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    code = data.get("message", "")

    if model is None or vectorizer is None:
        return jsonify({"reply": "❌ Model not loaded"})

    try:
        # ML Prediction
        X = vectorizer.transform([code])
        pred = model.predict(X)[0]
        prob = model.predict_proba(X)[0]

        risk_score = int(prob[1] * 100)
        label = "Vulnerable" if pred == 1 else "Safe"

        # GPT Explanation
        prompt = f"""
You are a cybersecurity expert AI.

Code:
{code}

ML Result:
- Prediction: {label}
- Risk Score: {risk_score}%

Explain:
1. Is it vulnerable?
2. Why?
3. Fix it
4. Give corrected code
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        explanation = response.choices[0].message.content

        return jsonify({
            "reply": explanation,
            "prediction": label,
            "risk": risk_score
        })

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)