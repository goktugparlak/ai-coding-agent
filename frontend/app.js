const form = document.querySelector("#chat-form");
const input = document.querySelector("#message-input");
const messages = document.querySelector("#messages");
const commandButtons = document.querySelectorAll("[data-command]");

function appendMessage(role, text) {
    const wrapper = document.createElement("div");
    wrapper.className = `message ${role}`;

    const label = document.createElement("div");
    label.className = "label";
    label.textContent = role === "user" ? "You" : "Agent";

    const body = document.createElement("pre");
    body.textContent = text;

    wrapper.append(label, body);
    messages.appendChild(wrapper);
    messages.scrollTop = messages.scrollHeight;
}

async function sendMessage(message) {
    appendMessage("user", message);

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message }),
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        appendMessage("agent", data.response);
    } catch (error) {
        appendMessage("agent", `Request failed: ${error.message}`);
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = input.value.trim();
    if (!message) return;

    input.value = "";
    await sendMessage(message);
    input.focus();
});

commandButtons.forEach((button) => {
    button.addEventListener("click", async () => {
        await sendMessage(button.dataset.command);
    });
});
