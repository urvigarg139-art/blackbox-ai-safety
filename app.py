import os
from flask import Flask, render_template, request, jsonify
import joblib
import google.generativeai as genai

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

# ---------- GEMINI SETUP ----------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
ai_model = genai.GenerativeModel("gemini-1.5-flash")

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- SCAN ----------
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

# ---------- CHAT (ML + GEMINI) ----------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    code = data.get("code", "")
    message = data.get("message", "")

    try:
        # ML Prediction
        X = vectorizer.transform([code])
        pred = model.predict(X)[0]
        prob = model.predict_proba(X)[0]

        label = "Vulnerable" if pred == 1 else "Safe"
        risk = int(prob[1] * 100)

        # Prompt for Gemini
        prompt = f"""
You are a cybersecurity expert AI.

Code:
{code}

ML Result:
{label} ({risk}% risk)

User question:
{message}

Explain:
- Is it vulnerable?
- Why?
- Fix it
- Give corrected code
"""

        response = ai_model.generate_content(prompt)
        reply = response.text

        return jsonify({
            "reply": reply,
            "prediction": label,
            "risk": risk
        })

    except Exception as e:
        return jsonify({
            "reply": "⚠️ AI unavailable. Please try again later."
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)