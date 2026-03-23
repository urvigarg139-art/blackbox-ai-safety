console.log("JS CONNECTED ✅");

// Wait until page fully loads
document.addEventListener("DOMContentLoaded", () => {

    const exampleBtn = document.getElementById("exampleBtn");
    const scanBtn = document.getElementById("scanBtn");

    exampleBtn.addEventListener("click", loadExample);
    scanBtn.addEventListener("click", scanCode);

});

// Load example
function loadExample() {
    document.getElementById("codeInput").value =
        "SELECT * FROM users WHERE id = ' + user_input + '";
}

// Scan code
async function scanCode() {

    const code = document.getElementById("codeInput").value;

    if (!code.trim()) {
        alert("Enter some code first");
        return;
    }

    const loader = document.getElementById("loader");
    const resultBox = document.getElementById("result");

    loader.style.display = "block";
    resultBox.style.display = "none";

    try {
        const response = await fetch("/scan", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code: code })
        });

        const data = await response.json();

        // Hide loader
        loader.style.display = "none";
        resultBox.style.display = "block";

        document.getElementById("label").innerText = data.label;
        document.getElementById("risk").innerText = "Risk: " + data.risk + "%";
        document.getElementById("confidence").innerText = "Confidence: " + data.confidence + "%";

    } catch (err) {
        console.error(err);
        loader.innerText = "❌ Error occurred";
    }
}