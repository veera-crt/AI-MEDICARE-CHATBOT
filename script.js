// Updated script.js with voice recognition

document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const voiceBtn = document.getElementById('voice-btn');
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    // Check if browser supports speech recognition
    if (!SpeechRecognition) {
        voiceBtn.style.display = 'none';
        console.warn('Speech recognition not supported in this browser');
    } else {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        // Voice status element
        const voiceStatus = document.createElement('div');
        voiceStatus.className = 'voice-status';
        document.body.appendChild(voiceStatus);
        
        voiceBtn.addEventListener('click', function() {
            if (voiceBtn.classList.contains('listening')) {
                recognition.stop();
                voiceBtn.classList.remove('listening');
                voiceStatus.style.display = 'none';
            } else {
                recognition.start();
                voiceBtn.classList.add('listening');
                voiceStatus.textContent = 'Listening...';
                voiceStatus.style.display = 'block';
            }
        });
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            voiceStatus.textContent = 'Processing...';
            
            // Auto-send after short delay
            setTimeout(() => {
                sendMessage();
                voiceStatus.style.display = 'none';
            }, 800);
        };
        
        recognition.onerror = function(event) {
            console.error('Speech recognition error', event.error);
            voiceBtn.classList.remove('listening');
            voiceStatus.textContent = 'Error: ' + event.error;
            setTimeout(() => voiceStatus.style.display = 'none', 2000);
        };
        
        recognition.onend = function() {
            voiceBtn.classList.remove('listening');
            if (voiceStatus.textContent === 'Listening...') {
                voiceStatus.style.display = 'none';
            }
        };
    }
    
    // Initial bot message
    setTimeout(() => {
        document.querySelector('.typing-animation').remove();
        addBotMessage("🤖 Hello! I'm MediCare Bot. I can help with medical-related queries. 💬 Type with >pain< suffix or speak your health question.");
    }, 1500);
    
    function addBotMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.innerHTML = `<div class="message-content">${text}</div>`;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        if (text.includes('🩺') || text.includes('⚠️')) {
            messageDiv.classList.add('glow-effect');
        }
    }
    
    function addUserMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        messageDiv.innerHTML = `<div class="message-content">${text}</div>`;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message';
        typingDiv.innerHTML = `
            <div class="message-content">
                <div class="typing-animation">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return typingDiv;
    }
    
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        addUserMessage(message);
        userInput.value = '';
        
        const typingIndicator = showTypingIndicator();
        
        try {
            const response = await fetch('https://ai-medicare-chatbot.onrender.com/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
                credentials: 'omit'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            typingIndicator.remove();
            addBotMessage(data.response);
        } catch (error) {
            console.error('Error:', error);
            typingIndicator.remove();
            addBotMessage("⚠️ Sorry, I'm having trouble connecting to the server. Please try again later.");
        }
    }
    
    sendBtn.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
