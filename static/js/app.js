let lastResult = null;
let scanHistory = JSON.parse(localStorage.getItem("history")) || [];

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("exampleBtn").onclick = loadExample;
    document.getElementById("scanBtn").onclick = scanCode;
    document.getElementById("downloadBtn").onclick = downloadReport;

    document.getElementById("historyBtn").onclick = showHistory;
    document.getElementById("scanTab").onclick = showScan;
});

function loadExample() {
    document.getElementById("codeInput").value =
        "SELECT * FROM users WHERE id = ' + user_input + '";
}

async function scanCode() {

    const code = document.getElementById("codeInput").value;

    if (!code.trim()) {
        alert("Enter code first");
        return;
    }

    const loader = document.getElementById("loader");
    const result = document.getElementById("result");

    loader.style.display = "block";
    result.style.display = "none";

    const res = await fetch("/scan", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({code})
    });

    const data = await res.json();
    lastResult = data;

    // Save history
    scanHistory.unshift(data);
    localStorage.setItem("history", JSON.stringify(scanHistory));

    loader.style.display = "none";
    result.style.display = "flex";

    typeText("label", data.label);
    typeText("risk", "Risk: " + data.risk + "%");
    typeText("confidence", "Confidence: " + data.confidence + "%");
    typeText("fix", data.fix);

    drawChart(data.risk, data.confidence);
}

function typeText(id, text) {
    let i = 0;
    const el = document.getElementById(id);
    el.innerText = "";

    const interval = setInterval(() => {
        el.innerText += text[i];
        i++;
        if (i >= text.length) clearInterval(interval);
    }, 15);
}

function drawChart(risk, confidence) {
    new Chart(document.getElementById("chart"), {
        type: "bar",
        data: {
            labels: ["Risk", "Confidence"],
            datasets: [{
                label: "Analysis",
                data: [risk, confidence]
            }]
        }
    });
}

async function downloadReport() {
    if (!lastResult) {
        alert("Run scan first!");
        return;
    }

    const res = await fetch("/download", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(lastResult)
    });

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "report.pdf";
    a.click();
}

function showHistory() {
    document.getElementById("historyPanel").style.display = "block";
    document.getElementById("result").style.display = "none";

    renderHistory();
}

function showScan() {
    document.getElementById("historyPanel").style.display = "none";
    document.getElementById("result").style.display = "flex";
}

function renderHistory() {
    const list = document.getElementById("historyList");
    list.innerHTML = "";

    scanHistory.forEach((item, index) => {
        const div = document.createElement("div");
        div.className = "card";
        div.innerHTML = `
            <b>Scan ${index + 1}</b><br>
            ${item.label}<br>
            Risk: ${item.risk}%<br>
            Confidence: ${item.confidence}%
        `;
        list.appendChild(div);
    });
}
// ================= USER PROFILE =================
let user = {
    name: "Urvi",
    avatar: "/static/default-avatar.png"
};

document.getElementById("username").innerText = user.name;
document.getElementById("userAvatar").src = user.avatar;


// ================= HISTORY =================
let history = JSON.parse(localStorage.getItem("chatHistory")) || [];

function addToHistory(text) {
    history.unshift(text);
    localStorage.setItem("chatHistory", JSON.stringify(history));
    renderHistory();
}

function renderHistory() {
    let container = document.getElementById("historyList");
    if (!container) return;

    container.innerHTML = "";

    history.forEach(item => {
        let div = document.createElement("div");
        div.className = "history-item";
        div.innerText = item;

        div.onclick = () => {
            loadChat(item);
        };

        container.appendChild(div);
    });
}

function loadChat(text) {
    console.log("Load:", text);
}

// Initial load
renderHistory();