function loadExample() {
    document.getElementById("codeInput").value =
        "SELECT * FROM users WHERE id = '" + " + user_input + '";
}

let latestData = null;

async function scanCode() {

    const code = document.getElementById("codeInput").value;

    document.getElementById("loader").innerText = "🤖 AI analyzing...";

    const res = await fetch("/scan", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ code })
    });

    const data = await res.json();
    latestData = data;

    document.getElementById("loader").innerText = "";

    document.getElementById("resultBox").style.display = "block";

    document.getElementById("resultText").innerText = data.result;
    document.getElementById("risk").innerText = data.risk;
    document.getElementById("confidence").innerText = data.confidence;

    document.getElementById("highlighted").innerText = data.highlighted;

    // vulnerabilities
    const vulnList = document.getElementById("vulnList");
    vulnList.innerHTML = "";
    data.vulnerabilities.forEach(v => {
        const li = document.createElement("li");
        li.innerText = `${v[0]} (Line ${v[2]+1})`;
        vulnList.appendChild(li);
    });

    // fixes
    const fixList = document.getElementById("fixList");
    fixList.innerHTML = "";
    data.fixes.forEach(f => {
        const li = document.createElement("li");
        li.innerText = f;
        fixList.appendChild(li);
    });

    renderChart(data.risk, data.confidence);
}


function renderChart(risk, confidence) {
    const ctx = document.getElementById('chart');

    if (window.myChart) window.myChart.destroy();

    window.myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Risk', 'Confidence'],
            datasets: [{
                data: [risk, confidence],
                backgroundColor: ['red', 'green']
            }]
        }
    });
}


async function downloadReport() {
    const res = await fetch("/download", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(latestData)
    });

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "report.pdf";
    a.click();
}