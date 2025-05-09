document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotWidget = document.getElementById('chatbot-widget');
    const chatbotClose = document.getElementById('chatbot-close');
    const chatbotMessages = document.getElementById('chatbot-messages');
    const chatbotInput = document.getElementById('chatbot-input-text');
    const chatbotSend = document.getElementById('chatbot-send');
    
    // Toggle chatbot visibility
    chatbotToggle.addEventListener('click', function(e) {
        e.preventDefault();
        if (chatbotWidget.style.display === 'flex') {
            chatbotWidget.style.display = 'none';
        } else {
            chatbotWidget.style.display = 'flex';
            // Focus the input when opening
            chatbotInput.focus();
        }
    });
    
    // Close chatbot
    chatbotClose.addEventListener('click', function() {
        chatbotWidget.style.display = 'none';
    });
    
    // Function to add a message to the chat
    function addMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender}-message`;
        
        // Check if message contains HTML or is just text
        if (message.includes('<') && message.includes('>')) {
            messageElement.innerHTML = message;
        } else {
            messageElement.textContent = message;
        }
        
        chatbotMessages.appendChild(messageElement);
        
        // Scroll to bottom
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }
    
    // Send message function
    function sendMessage() {
        const message = chatbotInput.value.trim();
        
        if (message === '') {
            return;
        }
        
        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input
        chatbotInput.value = '';
        
        // Show typing indicator
        const typingElement = document.createElement('div');
        typingElement.className = 'message bot-message typing-indicator';
        typingElement.textContent = 'Typing...';
        chatbotMessages.appendChild(typingElement);
        
        // Scroll to bottom
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        
        // Send message to backend
        fetch('/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            chatbotMessages.removeChild(typingElement);
            
            // Add bot response
            if (data.error) {
                addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            } else {
                addMessage(data.response, 'bot');
                
                // If there are suggested actions/quick replies
                if (data.suggestions && Array.isArray(data.suggestions) && data.suggestions.length > 0) {
                    const suggestionsContainer = document.createElement('div');
                    suggestionsContainer.className = 'suggestions-container';
                    
                    data.suggestions.forEach(suggestion => {
                        const suggestionBtn = document.createElement('button');
                        suggestionBtn.className = 'suggestion-btn';
                        suggestionBtn.textContent = suggestion;
                        suggestionBtn.addEventListener('click', function() {
                            chatbotInput.value = suggestion;
                            sendMessage();
                        });
                        suggestionsContainer.appendChild(suggestionBtn);
                    });
                    
                    chatbotMessages.appendChild(suggestionsContainer);
                }
            }
            
            // Scroll to bottom again after adding response
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        })
        .catch(error => {
            // Remove typing indicator
            chatbotMessages.removeChild(typingElement);
            
            // Add error message
            addMessage('Sorry, there was a network error. Please try again later.', 'bot');
            console.error('Error:', error);
        });
    }
    
    // Event listeners for sending messages
    chatbotSend.addEventListener('click', sendMessage);
    
    chatbotInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Add initial welcome message
    setTimeout(() => {
        addMessage('Hello! How can I help you today?', 'bot');
    }, 500);
});