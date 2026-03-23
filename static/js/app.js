let chart = null;
let lastResult = null;

function sendMessage() {
    let code = document.getElementById("inputBox").value;

    fetch("/scan", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({code})
    })
    .then(res => res.json())
    .then(data => {

        lastResult = data;

        document.getElementById("label").innerText = data.label;
        document.getElementById("risk").innerText = data.risk + "%";
        document.getElementById("confidence").innerText = data.confidence + "%";
        document.getElementById("fix").innerText = data.fix;

        document.getElementById("fixedCode").innerText = data.fixed_code;

        updateChart(data.risk, data.confidence);
        renderHistory();
    });
}

function updateChart(risk, confidence) {
    let ctx = document.getElementById("chart").getContext("2d");

    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Risk", "Confidence", "Safety"],
            datasets: [{
                data: [risk, confidence, 100 - risk],
                backgroundColor: ["red", "blue", "green"]
            }]
        }
    });
}

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
                sendMessage();
            };

            container.appendChild(div);
        });
    });
}

function loadExample() {
    document.getElementById("inputBox").value = "SELECT * FROM users WHERE id = ' + user_input + '";
}

function downloadReport() {
    fetch("/download", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(lastResult)
    })
    .then(res => res.blob())
    .then(blob => {
        let a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "report.pdf";
        a.click();
    });
}

document.addEventListener("DOMContentLoaded", renderHistory);