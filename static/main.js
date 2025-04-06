const socket = io();

function sendMessage() {
    const input = document.getElementById("input");
    const msg = input.value;
    if (!msg) return;

    addMessage("You: " + msg, "user");
    socket.emit("user_message", { message: msg });
    input.value = "";
}

socket.on("bot_reply", function(data) {
    addMessage("Bot: " + data.message, "bot");
});

function addMessage(text, cls) {
    const div = document.createElement("div");
    div.className = "msg " + cls;
    div.innerText = text;
    document.getElementById("messages").appendChild(div);
    document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
}
