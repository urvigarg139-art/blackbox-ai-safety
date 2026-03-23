let lastResult = null;
let chart = null;

// ================= SCAN =================
function sendMessage() {
    let code = document.getElementById("inputBox").value;

    fetch("/scan", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({code: code})
    })
    .then(res => res.json())
    .then(data => {

        lastResult = data;

        // TEXT OUTPUT
        document.getElementById("label").innerHTML =
            data.risk > 70 ? "⚠️ " + data.label : "✅ " + data.label;

        document.getElementById("risk").innerText = data.risk + "%";
        document.getElementById("confidence").innerText = data.confidence + "%";
        document.getElementById("fix").innerText = data.fix;

        // 🔥 DYNAMIC GLOW
        let cards = document.querySelector(".cards");

        if (data.risk > 70) {
            cards.style.boxShadow = "0 0 25px red, 0 0 50px rgba(255,0,0,0.6)";
        } else if (data.risk > 30) {
            cards.style.boxShadow = "0 0 25px orange";
        } else {
            cards.style.boxShadow = "0 0 25px green";
        }

        // 🔥 GRAPH FIX (IMPORTANT)
        updateChart(data.risk, data.confidence);

        renderHistory();
    });
}


// ================= GRAPH =================
function updateChart(risk, confidence) {
    let canvas = document.getElementById("chart");

    if (!canvas) return;

    let ctx = canvas.getContext("2d");

    if (chart) {
        chart.destroy();
    }

    let safety = 100 - risk;

    chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Risk", "Confidence", "Safety"],
            datasets: [{
                label: "Analysis %",
                data: [risk, confidence, safety],
                backgroundColor: [
                    "rgba(255, 0, 0, 0.7)",     // Risk
                    "rgba(0, 200, 255, 0.7)",   // Confidence
                    "rgba(0, 255, 100, 0.7)"    // Safety
                ],
                borderRadius: 10
            }]
        },
        options: {
            responsive: true,
            animation: {
                duration: 800
            },
            plugins: {
                legend: {
                    labels: { color: "white" }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: "white" }
                },
                x: {
                    ticks: { color: "white" }
                }
            }
        }
    });
}


// ================= HISTORY =================
function renderHistory() {
    fetch("/get_history")
    .then(res => res.json())
    .then(data => {

        let container = document.getElementById("historyList");
        if (!container) return;

        container.innerHTML = "";

        data.forEach(item => {
            let div = document.createElement("div");
            div.className = "history-item";
            div.innerText = item;

            div.onclick = () => {
                document.getElementById("inputBox").value = item;
                sendMessage();

                document.querySelectorAll(".history-item").forEach(el => {
                    el.classList.remove("active");
                });

                div.classList.add("active");
            };

            container.appendChild(div);
        });
    });
}


// ================= BUTTONS =================
function loadExample() {
    document.getElementById("inputBox").value = `
// ================= INSECURE WEB APP EXAMPLE =================

// Node.js + Express (Vulnerable Backend)

const express = require("express");
const app = express();
const mysql = require("mysql");

const db = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "",
    database: "users_db"
});

// ❌ VULNERABLE LOGIN (SQL Injection)
app.get("/login", (req, res) => {
    const username = req.query.username;
    const password = req.query.password;

    const query = "SELECT * FROM users WHERE username = '" 
        + username + "' AND password = '" + password + "'";

    db.query(query, (err, result) => {
        if (err) throw err;

        if (result.length > 0) {
            res.send("Login Successful");
        } else {
            res.send("Invalid Credentials");
        }
    });
});


// ❌ VULNERABLE SEARCH FUNCTION
app.get("/search", (req, res) => {
    const keyword = req.query.keyword;

    const query = "SELECT * FROM products WHERE name LIKE '%" 
        + keyword + "%'";

    db.query(query, (err, result) => {
        res.send(result);
    });
});


// ❌ COMMAND INJECTION (VERY CRITICAL)
const { exec } = require("child_process");

app.get("/ping", (req, res) => {
    const ip = req.query.ip;

    exec("ping " + ip, (err, stdout) => {
        res.send(stdout);
    });
});


// ❌ XSS (Cross Site Scripting)
app.get("/profile", (req, res) => {
    const name = req.query.name;

    res.send("<h1>Welcome " + name + "</h1>");
});


// ❌ HARD-CODED SECRET (BAD PRACTICE)
const API_KEY = "123456SECRETKEY";


// SERVER START
app.listen(3000, () => {
    console.log("Server running on port 3000");
});
`;
}

function downloadReport() {
    if (!lastResult) return alert("Run scan first!");

    fetch("/download", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(lastResult)
    })
    .then(res => res.blob())
    .then(blob => {
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement("a");
        a.href = url;
        a.download = "report.pdf";
        a.click();
    });
}

function toggleHistory() {
    let panel = document.getElementById("historyPanel");
    panel.style.display = panel.style.display === "block" ? "none" : "block";
}

function newScan() {
    document.getElementById("inputBox").value = "";
    document.getElementById("label").innerText = "";
    document.getElementById("risk").innerText = "";
    document.getElementById("confidence").innerText = "";
    document.getElementById("fix").innerText = "";

    let cards = document.querySelector(".cards");
    if (cards) cards.style.boxShadow = "none";
}

function clearHistory() {
    fetch("/clear_history", { method: "POST" })
    .then(() => renderHistory());
}


// INIT
document.addEventListener("DOMContentLoaded", renderHistory);