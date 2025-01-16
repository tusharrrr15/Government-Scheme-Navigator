// Selectors for chatbot elements
const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector("#send-btn");

// Variable to store the user's message
let userMessage = null;

// Initial height of the input textarea
const inputInitHeight = chatInput.scrollHeight;

// Chatbot endpoint URL on your Flask server
const API_URL = "/chatbot";

// Function to create a chat <li> element
const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", className);
    let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").textContent = message;
    return chatLi;
};

// Function to generate a response from the Flask server
const generateResponse = (chatElement) => {
    const messageElement = chatElement.querySelector("p");

    // Define the properties and body for the API request
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userMessage })
    };

    // Send POST request to the Flask server, handle response, and update the chatbox
    fetch(API_URL, requestOptions)
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                messageElement.textContent = data.response.trim(); // Set the response in the chat element
            } else {
                messageElement.classList.add("error");
                messageElement.textContent = "Sorry, I couldn't process your request.";
            }
        })
        .catch(() => {
            messageElement.classList.add("error");
            messageElement.textContent = "Oops! Something went wrong. Please try again.";
        })
        .finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
};

// Function to handle user chat messages
const handleChat = () => {
    userMessage = chatInput.value.trim(); // Get user's message
    if (!userMessage) return;

    // Clear the input and reset its height
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Append the user's message to the chatbox
    const outgoingChatLi = createChatLi(userMessage, "outgoing");
    chatbox.appendChild(outgoingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);

    // Create an incoming chat element to display "Thinking..."
    setTimeout(() => {
        const incomingChatLi = createChatLi("Thinking...", "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi);
    }, 600);
};

// Event listeners
chatInput.addEventListener("input", () => {
    // Adjust the height of the input textarea based on its content
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    // Handle Enter key for sending messages (prevent default and handle chat)
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

sendChatBtn.addEventListener("click", handleChat);
closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));
