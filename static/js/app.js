async function scanCode() {
    let code = document.getElementById("code").value;

    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("result").classList.add("hidden");

    let res = await fetch("/scan", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({code: code})
    });

    let data = await res.json();

    document.getElementById("loading").classList.add("hidden");
    document.getElementById("result").classList.remove("hidden");

    document.getElementById("label").innerText = data.label;
    document.getElementById("risk").innerText = data.risk + "%";
    document.getElementById("confidence").innerText = data.confidence + "%";
    document.getElementById("reason").innerText = data.reason;
    document.getElementById("fix").innerText = data.fix;

    document.getElementById("riskBar").style.width = data.risk + "%";
    document.getElementById("confBar").style.width = data.confidence + "%";

    new Chart(document.getElementById("chart"), {
        type: "bar",
        data: {
            labels: ["Risk", "Confidence"],
            datasets: [{
                label: "Analysis",
                data: [data.risk, data.confidence]
            }]
        }
    });
}

function loadExample() {
    document.getElementById("code").value =
        "SELECT * FROM users WHERE id = ' + user_input + '";
}