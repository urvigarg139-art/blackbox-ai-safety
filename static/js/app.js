async function scanCode() {

    let code = document.getElementById("code").value;

    document.getElementById("loading").classList.remove("hidden");

    let res = await fetch("/scan", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({code})
    });

    let data = await res.json();

    document.getElementById("loading").classList.add("hidden");
    document.getElementById("result").classList.remove("hidden");

    document.getElementById("label").innerText = data.label;
    document.getElementById("risk").innerText = data.risk + "%";
    document.getElementById("confidence").innerText = data.confidence + "%";
    document.getElementById("reason").innerText = data.reason;
    document.getElementById("fix").innerText = data.fix;
}

function loadExample() {
    document.getElementById("code").value =
        "SELECT * FROM users WHERE id = ' + user_input + '";
}