from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    code = data.get("code", "")

    # Dummy ML logic
    if "SELECT" in code:
        result = "Vulnerable"
        risk = 62.9
        confidence = 37.1
        suggestion = "Use parameterized queries to prevent SQL Injection."
    else:
        result = "Safe"
        risk = 10
        confidence = 90
        suggestion = "Code looks safe. Keep validating inputs."

    return jsonify({
        "result": result,
        "risk": risk,
        "confidence": confidence,
        "code": code,
        "suggestion": suggestion
    })


if __name__ == "__main__":
    app.run(debug=True)