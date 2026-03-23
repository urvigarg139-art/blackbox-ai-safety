let lastResult = null;

// SCAN
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

        document.getElementById("label").innerText = data.label;
        document.getElementById("risk").innerText = data.risk + "%";
        document.getElementById("confidence").innerText = data.confidence + "%";
        document.getElementById("fix").innerText = data.fix;

        renderHistory();
        updateChart(data.risk);
    });
}

// HISTORY (DB)
function renderHistory() {
    fetch("/get_history")
    .then(res => res.json())
    .then(data => {
        let container = document.getElementById("historyList");
        container.innerHTML = "";

        data.forEach(item => {
            let div = document.createElement("div");
            div.className = "history-item";
            div.innerText = item;

            div.onclick = () => {
                document.getElementById("inputBox").value = item;
            };

            container.appendChild(div);
        });
    });
}

function toggleHistory() {
    let panel = document.getElementById("historyPanel");
    panel.style.display = panel.style.display === "block" ? "none" : "block";
}

// BUTTONS
function loadExample() {
    document.getElementById("inputBox").value =
        "SELECT * FROM users WHERE id = ' + user_input + '";
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

// CHART
let chart;
function updateChart(risk) {
    let ctx = document.getElementById("chart").getContext("2d");

    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Risk"],
            datasets: [{
                label: "Risk %",
                data: [risk]
            }]
        }
    });
}

// INIT
document.addEventListener("DOMContentLoaded", renderHistory);