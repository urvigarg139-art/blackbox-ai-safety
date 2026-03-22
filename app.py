import os
from flask import Flask, render_template, request, jsonify
import joblib
import google.generativeai as genai

app = Flask(__name__)

# ---------------- LOAD MODEL ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
    vectorizer = joblib.load(os.path.join(BASE_DIR, "vector.pkl"))
    print("✅ Model loaded")
except Exception as e:
    print("❌ Model error:", e)
    model = None
    vectorizer = None

# ---------------- GEMINI SETUP ----------------
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    ai_model = genai.GenerativeModel("gemini-1.5-flash")
    print("✅ Gemini ready")
except Exception as e:
    print("❌ Gemini error:", e)
    ai_model = None


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- SCAN ----------------
@app.route("/scan", methods=["POST"])
def scan():
    code = request.form.get("code")

    if not code:
        return render_template("index.html", error="⚠️ No code provided")

    try:
        if model and vectorizer:
            vec = vectorizer.transform([code])
            pred = model.predict(vec)[0]
            prob = model.predict_proba(vec)[0][1]

            result = "Vulnerable" if pred == 1 else "Safe"
            risk_score = round(prob * 100, 2)
            confidence = round((1 - prob) * 100, 2)
        else:
            result = "Model not available"
            risk_score = 0
            confidence = 0

    except Exception as e:
        print("❌ Scan error:", e)
        result = "Error during scan"
        risk_score = 0
        confidence = 0

    return render_template(
        "dashboard.html",
        code=code,
        result=result,
        risk_score=risk_score,
        confidence=confidence
    )


# ---------------- CHAT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        message = data.get("message", "")
        code = data.get("code", "")

        if not message:
            return jsonify({"reply": "⚠️ Enter a question"})

        if not ai_model:
            return jsonify({"reply": "⚠️ AI not configured properly"})

        prompt = f"""
You are a security assistant.

Code:
{code}

User question:
{message}

Explain vulnerabilities clearly and suggest fixes.
"""

        response = ai_model.generate_content(prompt)

        if not response.text:
            return jsonify({"reply": "⚠️ Empty response from AI"})

        return jsonify({"reply": response.text})

    except Exception as e:
        print("❌ GEMINI ERROR:", e)
        return jsonify({"reply": f"⚠️ Error: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)