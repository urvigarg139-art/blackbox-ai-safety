async function sendMessage() {
    const input = document.getElementById("chatInput");
    const chatBox = document.getElementById("chatBox");

    const message = input.value;
    const code = document.getElementById("codeInput").value;

    chatBox.innerHTML += `<div class="user-msg">👤 ${message}</div>`;

    const res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message, code })
    });

    const data = await res.json();

    chatBox.innerHTML += `<div class="ai-msg">🤖 ${data.reply}</div>`;

    input.value = "";
}