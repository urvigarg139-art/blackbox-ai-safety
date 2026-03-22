function loadExample() {
    document.getElementById("codeInput").value =
        "SELECT * FROM users WHERE id = '" + " + user_input + '";
}


async function scanCode() {

    const code = document.getElementById("codeInput").value;

    if (!code) {
        alert("Enter code first");
        return;
    }

    // loader animation
    let width = 0;
    const bar = document.getElementById("loaderBar");
    bar.style.width = "0%";

    const interval = setInterval(() => {
        if (width >= 100) clearInterval(interval);
        else {
            width++;
            bar.style.width = width + "%";
        }
    }, 10);

    const res = await fetch("/scan", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ code })
    });

    const data = await res.json();

    // show result
    document.getElementById("resultBox").style.display = "block";
    document.getElementById("chartBox").style.display = "block";

    document.getElementById("resultText").innerText =
        data.result === "Vulnerable"
            ? "⚠️ Vulnerability Detected"
            : "✅ Code is Safe";

    document.getElementById("risk").innerText = data.risk;
    document.getElementById("confidence").innerText = data.confidence;
    document.getElementById("codeOutput").innerText = data.code;

    // vulnerabilities
    const vulnBox = document.getElementById("vulnBox");
    const vulnList = document.getElementById("vulnList");

    vulnList.innerHTML = "";

    if (data.vulnerabilities.length > 0) {
        vulnBox.style.display = "block";

        data.vulnerabilities.forEach(v => {
            const li = document.createElement("li");
            li.innerText = `${v[0]} (Risk: ${v[1]}%)`;
            vulnList.appendChild(li);
        });

    } else {
        vulnBox.style.display = "none";
    }

    // fixes
    const fixBox = document.getElementById("fixBox");
    const fixList = document.getElementById("fixList");

    fixList.innerHTML = "";

    if (data.fixes.length > 0) {
        fixBox.style.display = "block";

        data.fixes.forEach(f => {
            const li = document.createElement("li");
            li.innerText = f;
            fixList.appendChild(li);
        });

    } else {
        fixBox.style.display = "none";
    }

    renderChart(data.risk, data.confidence);
}


// chart
function renderChart(risk, confidence) {

    const ctx = document.getElementById('chart');

    if (window.myChart) window.myChart.destroy();

    window.myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Risk', 'Confidence'],
            datasets: [{
                data: [risk, confidence],
                backgroundColor: ['#ef4444', '#22c55e']
            }]
        }
    });
}