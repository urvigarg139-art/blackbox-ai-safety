from flask import Flask,render_template,jsonify,send_file
import datetime
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run_audit",methods=["POST"])
def run():

    case_id = str(uuid.uuid4())[:8]
    time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

    result = {
        "case_id":case_id,
        "time":time,
        "risk":82,
        "severity":"CRITICAL",
        "location":"(2,3)",
        "findings":[
            "Reward manipulation detected",
            "Prompt injection vulnerability",
            "Unsafe optimization loop"
        ]
    }

    with open("logs/exploits.txt","w") as f:
        f.write(str(result))

    return jsonify(result)

@app.route("/download")
def download():
    return send_file("logs/exploits.txt",as_attachment=True)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)










