function loadExample() {
    document.getElementById("code").value =
        "SELECT * FROM users WHERE id = ' + user_input + '";
}

async function scanCode() {

    let code = document.getElementById("code").value;

    document.getElementById("loading").style.display = "block";

    let res = await fetch("/scan", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({code: code})
    });

    let data = await res.json();

    document.getElementById("loading").style.display = "none";
    document.getElementById("result").style.display = "block";

    document.getElementById("label").innerText = data.label;
    document.getElementById("risk").innerText = "Risk: " + data.risk + "%";
    document.getElementById("confidence").innerText = "Confidence: " + data.confidence + "%";
}