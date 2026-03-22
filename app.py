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

# ---------- SCAN (ML ONLY) ----------
@app.route("/scan", methods=["POST"])
def scan():
    data = request.json
    code = data.get("code", "")

    if model is None or vectorizer is None:
        return jsonify({"error": "Model not loaded"})

    X = vectorizer.transform([code])
    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0]

    return jsonify({
        "prediction": int(pred),
        "risk": float(prob[1] * 100),
        "confidence": float(max(prob) * 100)
    })

# ---------- CHAT (ML + GPT) ----------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    code = data.get("code", "")
    message = data.get("message", "")

    try:
        # ML
        X = vectorizer.transform([code])
        pred = model.predict(X)[0]
        prob = model.predict_proba(X)[0]

        label = "Vulnerable" if pred == 1 else "Safe"
        risk = int(prob[1] * 100)

        # GPT
        prompt = f"""
You are a cybersecurity AI.

Code:
{code}

ML Result:
{label} ({risk}% risk)

User question:
{message}

Explain vulnerability, fix it, and give corrected code.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return jsonify({
            "reply": response.choices[0].message.content,
            "prediction": label,
            "risk": risk
        })

    except Exception as e:
        return jsonify({"reply": str(e)})

if __name__ == "__main__":
    app.run(debug=True)