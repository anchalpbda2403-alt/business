/* GramBiz AI - Advisor Chatbot Handler */

document.addEventListener('DOMContentLoaded', () => {
  const chatMessages = document.getElementById('chatMessages');
  const chatInput = document.getElementById('chatInput');
  const chatSendBtn = document.getElementById('chatSendBtn');

  if (!chatMessages || !chatInput || !chatSendBtn) return;

  // Load past chat history
  loadChatHistory();

  // Send message event
  chatSendBtn.addEventListener('click', sendMessage);
  chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });

  // Quick Action Chips / Buttons
  document.querySelectorAll('.advisor-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const text = chip.getAttribute('data-prompt') || chip.textContent.trim();
      chatInput.value = text;
      sendMessage();
    });
  });

  async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    // Append user message
    appendMessage(text, 'user');
    chatInput.value = '';

    // Typing indicator
    const typingElem = appendTypingIndicator();

    // Call API
    const res = await GramBiz.fetch('/business-advice', {
      method: 'POST',
      body: JSON.stringify({ message: text })
    });

    typingElem.remove();

    if (res.success && res.data && res.data.reply) {
      appendMessageWithTyping(res.data.reply, 'assistant');
    } else {
      appendMessage('I am currently experiencing connection issues. Please try again shortly.', 'assistant');
    }
  }

  function appendMessage(content, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-bubble chat-bubble-${sender}`;
    
    if (sender === 'assistant') {
      msgDiv.innerHTML = `
        <div class="chat-avatar"><i class="fas fa-robot"></i></div>
        <div class="chat-text">${formatMarkdownText(content)}</div>
      `;
    } else {
      msgDiv.innerHTML = `
        <div class="chat-text">${escapeHtml(content)}</div>
        <div class="chat-avatar user"><i class="fas fa-user"></i></div>
      `;
    }

    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function appendMessageWithTyping(content, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-bubble chat-bubble-${sender}`;
    msgDiv.innerHTML = `
      <div class="chat-avatar"><i class="fas fa-robot"></i></div>
      <div class="chat-text"></div>
    `;

    chatMessages.appendChild(msgDiv);
    const textElem = msgDiv.querySelector('.chat-text');

    let i = 0;
    const formatted = formatMarkdownText(content);
    textElem.innerHTML = formatted; // Set directly or stream if text
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function appendTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-bubble chat-bubble-assistant typing-bubble';
    typingDiv.innerHTML = `
      <div class="chat-avatar"><i class="fas fa-robot"></i></div>
      <div class="chat-text"><span class="typing-dots"><span>.</span><span>.</span><span>.</span></span></div>
    `;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return typingDiv;
  }

  async function loadChatHistory() {
    const res = await GramBiz.fetch('/chat-history');
    if (res.success && res.data && res.data.history && res.data.history.length > 0) {
      chatMessages.innerHTML = '';
      res.data.history.forEach(msg => {
        appendMessage(msg.message, msg.sender);
      });
    }
  }

  function formatMarkdownText(text) {
    let html = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n\n/g, '<br><br>')
      .replace(/\n/g, '<br>');
    return html;
  }

  function escapeHtml(text) {
    return text.replace(/[&<>"']/g, function(m) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[m];
    });
  }
});
