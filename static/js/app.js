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

        document.getElementById("label").innerHTML =
            data.risk > 70 ? "⚠️ " + data.label : "✅ " + data.label;

        document.getElementById("risk").innerText = data.risk + "%";
        document.getElementById("confidence").innerText = data.confidence + "%";
        document.getElementById("fix").innerText = data.fix;

        // Dynamic glow
        let cards = document.querySelector(".cards");

        if (data.risk > 70) {
            cards.style.boxShadow = "0 0 25px red, 0 0 50px rgba(255,0,0,0.6)";
        } else if (data.risk > 30) {
            cards.style.boxShadow = "0 0 25px orange";
        } else {
            cards.style.boxShadow = "0 0 25px green";
        }

        renderHistory();
        updateChart(data.risk);
    });
}

// HISTORY
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

                document.querySelectorAll(".history-item").forEach(el => {
                    el.classList.remove("active");
                });

                div.classList.add("active");
            };

            container.appendChild(div);
        });
    });
}

// NEW SCAN
function newScan() {
    document.getElementById("inputBox").value = "";
    document.getElementById("label").innerText = "";
    document.getElementById("risk").innerText = "";
    document.getElementById("confidence").innerText = "";
    document.getElementById("fix").innerText = "";

    document.querySelector(".cards").style.boxShadow = "none";
}

// CLEAR HISTORY
function clearHistory() {
    fetch("/clear_history", { method: "POST" })
    .then(() => renderHistory());
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