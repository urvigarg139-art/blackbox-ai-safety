console.log("🔥 UI READY");

// Ensure DOM ready
document.addEventListener("DOMContentLoaded", () => {

    document.getElementById("exampleBtn").addEventListener("click", loadExample);
    document.getElementById("scanBtn").addEventListener("click", scanCode);

});

// Load Example
function loadExample() {
    document.getElementById("codeInput").value =
        "SELECT * FROM users WHERE id = ' + user_input + '";
}

// Scan Function
async function scanCode() {

    const code = document.getElementById("codeInput").value;

    if (!code.trim()) {
        alert("Enter code first");
        return;
    }

    const loader = document.getElementById("loader");
    const result = document.getElementById("result");

    loader.style.display = "block";
    result.style.display = "none";

    try {
        const response = await fetch("/scan", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({code})
        });

        const data = await response.json();

        loader.style.display = "none";
        result.style.display = "flex";

        // Typing animation
        typeText("label", data.label);
        typeText("risk", "Risk: " + data.risk + "%");
        typeText("confidence", "Confidence: " + data.confidence + "%");

    } catch (err) {
        loader.innerText = "Error ❌";
    }
}

// Typing Effect
function typeText(id, text) {
    let i = 0;
    const el = document.getElementById(id);
    el.innerText = "";

    const interval = setInterval(() => {
        el.innerText += text[i];
        i++;
        if (i >= text.length) clearInterval(interval);
    }, 20);
}