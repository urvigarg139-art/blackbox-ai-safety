function loadExample() {
    const example = `SELECT * FROM users WHERE id = '` + "user_input" + `'`;
    document.getElementById("codeInput").value = example;
}

async function scanCode() {

    const code = document.getElementById("codeInput").value;

    if (!code) {
        alert("Please enter code");
        return;
    }

    // show loading
    document.getElementById("loading").style.display = "block";
    document.getElementById("resultBox").style.display = "none";

    const res = await fetch("/scan", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ code: code })
    });

    const data = await res.json();

    // hide loading
    document.getElementById("loading").style.display = "none";

    // show result
    document.getElementById("resultBox").style.display = "block";

    // typing animation
    typeText("resultText",
        data.result === "Vulnerable"
            ? "⚠️ Vulnerability Detected"
            : "✅ Code is Safe"
    );

    document.getElementById("risk").innerText = data.risk;
    document.getElementById("confidence").innerText = data.confidence;
    document.getElementById("codeOutput").innerText = data.code;

    typeText("suggestion", data.suggestion);

    renderChart(data.risk, data.confidence);
}


// typing effect
function typeText(id, text) {
    const el = document.getElementById(id);
    el.innerHTML = "";
    let i = 0;

    function typing() {
        if (i < text.length) {
            el.innerHTML += text.charAt(i);
            i++;
            setTimeout(typing, 20);
        }
    }

    typing();
}


// chart
function renderChart(risk, confidence) {

    const ctx = document.getElementById('chart');

    if (window.myChart) {
        window.myChart.destroy();
    }

    window.myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Risk', 'Confidence'],
            datasets: [{
                label: 'Analysis',
                data: [risk, confidence],
                backgroundColor: ['#ef4444', '#22c55e']
            }]
        }
    });
}