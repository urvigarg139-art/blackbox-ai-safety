let lastResult = null;

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("exampleBtn").onclick = loadExample;
    document.getElementById("scanBtn").onclick = scanCode;
    document.getElementById("downloadBtn").onclick = downloadReport;
});

function loadExample() {
    document.getElementById("codeInput").value =
        "SELECT * FROM users WHERE id = ' + user_input + '";
}

async function scanCode() {

    const code = document.getElementById("codeInput").value;
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