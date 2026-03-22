function loadExample() {
    document.getElementById("codeInput").value =
        "SELECT * FROM users WHERE id = '" + " + user_input + '";
}

async function sendMessage() {
    const input = document.getElementById("chatInput");
    const chatBox = document.getElementById("chatBox");
    const code = document.getElementById("codeInput").innerText;

    const message = input.value;

    if (!message) return;

    chatBox.innerHTML += `<div class="user-msg">👤 ${message}</div>`;

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ message, code })
        });

        const data = await res.json();

        chatBox.innerHTML += `<div class="ai-msg">🤖 ${data.reply}</div>`;
    } catch (err) {
        chatBox.innerHTML += `<div class="error">⚠️ Server error</div>`;
    }

    input.value = "";
}