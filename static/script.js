document.getElementById("chat-form").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent page reload

    let userInputField = document.getElementById("user_input");
    let userInput = userInputField.value.trim();
    
    if (userInput === "") return;  // Prevent empty messages

    let chatBox = document.getElementById("chat-box");

    // Display user message
    let userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = userInput;
    chatBox.appendChild(userMessage);

    // Clear the input field immediately
    userInputField.value = "";
    userInputField.focus();

    // Send input to Flask server
    fetch("/", {
        method: "POST",
        body: new URLSearchParams({ user_input: userInput }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    })
    .then(response => response.text())
    .then(data => {
        let parser = new DOMParser();
        let doc = parser.parseFromString(data, "text/html");
        let newChatBox = doc.getElementById("chat-box").innerHTML;

        chatBox.innerHTML = newChatBox;
        chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to bottom
    });
});
