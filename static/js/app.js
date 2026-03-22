function loadExample() {
    const textarea = document.getElementById("codeInput");

    textarea.value = "SELECT * FROM users WHERE id = '" + " + user_input + '";
}


async function sendMessage() {
    const input = document.getElementById("chatInput");
    const chatBox = document.getElementById("chatBox");
    const code = document.getElementById("codeDisplay").innerText;

    const message = input.value;

    if (!message) return;

    chatBox.innerHTML += `<div class="user">👤 ${message}</div>`;

    const res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message, code })
    });

    const data = await res.json();

    chatBox.innerHTML += `<div class="ai">🤖 ${data.reply}</div>`;

    input.value = "";
}