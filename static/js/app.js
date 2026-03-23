console.log("JS LOADED ✅");

// Load example code
function loadExample() {
    document.getElementById("codeInput").value =
        "SELECT * FROM users WHERE id = ' + user_input + '";
}

// Scan function
async function scanCode() {
    const code = document.getElementById("codeInput").value;

    if (!code.trim()) {
        alert("Please enter code");
        return;
    }

    // Show loading
    document.getElementById("result").style.display = "block";
    document.getElementById("label").innerText = "Analyzing...";
    document.getElementById("risk").innerText = "";
    document.getElementById("confidence").innerText = "";

    try {
        const response = await fetch("/scan", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code: code })
        });

        const data = await response.json();

        document.getElementById("label").innerText = data.label;
        document.getElementById("risk").innerText = "Risk: " + data.risk + "%";
        document.getElementById("confidence").innerText = "Confidence: " + data.confidence + "%";

    } catch (error) {
        console.error(error);
        document.getElementById("label").innerText = "Error occurred ❌";
    }
}