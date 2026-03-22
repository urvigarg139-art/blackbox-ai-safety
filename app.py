from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ---------- ANALYSIS ----------
def analyze_code(code):

    vulnerabilities = []

    if "SELECT" in code and "user_input" in code:
        vulnerabilities.append(("SQL Injection", 80))

    if "<script>" in code:
        vulnerabilities.append(("XSS Attack", 70))

    if "os.system" in code:
        vulnerabilities.append(("Command Injection", 85))

    if "password =" in code:
        vulnerabilities.append(("Hardcoded Secret", 60))

    if vulnerabilities:
        result = "Vulnerable"
        risk = max(v[1] for v in vulnerabilities)
        confidence = 100 - risk
    else:
        result = "Safe"
        risk = 10
        confidence = 90

    return result, risk, confidence, vulnerabilities


def generate_fix(vuln):
    fixes = {
        "SQL Injection": "Use parameterized queries instead of string concatenation.",
        "XSS Attack": "Escape user inputs before rendering in HTML.",
        "Command Injection": "Avoid os.system, use subprocess safely.",
        "Hardcoded Secret": "Store secrets in environment variables."
    }
    return fixes.get(vuln, "Follow secure coding practices.")


# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    code = data.get("code", "")

    result, risk, confidence, vulnerabilities = analyze_code(code)

    fixes = [generate_fix(v[0]) for v in vulnerabilities]

    return jsonify({
        "result": result,
        "risk": risk,
        "confidence": confidence,
        "code": code,
        "vulnerabilities": vulnerabilities,
        "fixes": fixes
    })


if __name__ == "__main__":
    app.run(debug=True)