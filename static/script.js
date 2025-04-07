// document.addEventListener("DOMContentLoaded", function () {
//     // Get all input fields with placeholders
//     const inputs = document.querySelectorAll(".input-group input");
//     inputs.forEach(input => {
//         // When the user starts typing, hide the placeholder
//         input.addEventListener("input", function () {
//             if (input.value.trim() !== "") {
//                 input.setAttribute("data-placeholder-hidden", "true");
//             } else {
//                 input.removeAttribute("data-placeholder-hidden");
//             }
//         });

//         // Restore placeholder when the input loses focus and is empty
//         input.addEventListener("blur", function () {
//             if (input.value.trim() === "") {
//                 input.removeAttribute("data-placeholder-hidden");
//             }
//         });
//     });

//     // Scroll to the bottom of the chat box
//     function scrollToBottom() {
//         const chatBox = document.getElementById('chat-box');
//         if (chatBox) {
//             chatBox.scrollTop = chatBox.scrollHeight;
//         }
//     }

//     // Scroll to bottom when the page loads
//     scrollToBottom();

//     // Scroll to bottom after submitting a message
//     const chatForm = document.getElementById('chat-form');
//     if (chatForm) {
//         chatForm.addEventListener('submit', function () {
//             setTimeout(scrollToBottom, 100); // Delay to allow message rendering
//         });
//     }

//     // Clear Chat Button Logic
//     const clearChatButton = document.getElementById('clear-chat');
//     if (clearChatButton) {
//         clearChatButton.addEventListener('click', function () {
//             if (confirm("Are you sure you want to clear your chat history?")) {
//                 fetch('/clear-chat', { method: 'POST' })
//                     .then(response => response.json())
//                     .then(data => {
//                         if (data.success) {
//                             location.reload(); // Reload the page to reflect the cleared chat
//                         } else {
//                             alert(`Error clearing chat: ${data.error}`);
//                         }
//                     })
//                     .catch(error => {
//                         console.error("Error:", error);
//                         alert("An unexpected error occurred while clearing the chat.");
//                     });
//             }
//         });
//     }
//     document.getElementById('go-back-button').addEventListener('click', function () {
//         window.location.href = "{{ url_for('index') }}";
//     });
// });

// function validatePhoneNumber(input) {
//     if (!input.value.startsWith("+91 ")) {
//         input.value = "+91 ";
//     }
// }

