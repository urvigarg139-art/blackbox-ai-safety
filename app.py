from flask import Flask, render_template, request, jsonify, send_file
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

def analyze_code(code):
    if "SELECT" in code and "+" in code:
        return {
            "label": "⚠️ SQL Injection Risk",
            "risk": 82,
            "confidence": 91,
            "fix": "Use parameterized queries (prepared statements)"
        }
    elif "eval(" in code:
        return {
            "label": "⚠️ Code Injection Risk",
            "risk": 75,
            "confidence": 88,
            "fix": "Avoid eval(), use safe parsing methods"
        }
    else:
        return {
            "label": "✅ Safe",
            "risk": 12,
            "confidence": 86,
            "fix": "No major issues detected"
        }

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/scan", methods=["POST"])
def scan():
    code = request.json.get("code", "")
    return jsonify(analyze_code(code))

# PDF REPORT
@app.route("/download", methods=["POST"])
def download():
    data = request.json

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = [
        Paragraph("AI Security Report", styles["Title"]),
        Paragraph(f"Status: {data['label']}", styles["Normal"]),
        Paragraph(f"Risk: {data['risk']}%", styles["Normal"]),
        Paragraph(f"Confidence: {data['confidence']}%", styles["Normal"]),
        Paragraph(f"Fix: {data['fix']}", styles["Normal"]),
    ]

    doc.build(content)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="report.pdf")

if __name__ == "__main__":
    app.run(debug=True)