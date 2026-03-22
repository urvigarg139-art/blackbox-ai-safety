document.addEventListener("DOMContentLoaded", () => {

    const scanBtn = document.getElementById("scanBtn");
    const exampleBtn = document.getElementById("exampleBtn");

    scanBtn.addEventListener("click", scanCode);
    exampleBtn.addEventListener("click", loadExample);

});

function loadExample() {
    document.getElementById("code").value =
        "SELECT * FROM users WHERE id = ' + user_input + '";
}

async function scanCode() {

    let code = document.getElementById("code").value;

    if (!code) {
        alert("Paste code first!");
        return;
    }

    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("result").classList.add("hidden");

    try {
        let res = await fetch("/scan", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({code: code})
        });

        let data = await res.json();

        document.getElementById("label").innerText = data.label;
        document.getElementById("risk").innerText = data.risk;
        document.getElementById("confidence").innerText = data.confidence;
        document.getElementById("reason").innerText = data.reason;
        document.getElementById("fix").innerText = data.fix;

        document.getElementById("loading").classList.add("hidden");
        document.getElementById("result").classList.remove("hidden");

    } catch (err) {
        console.error(err);
        alert("Scan failed");
    }
}