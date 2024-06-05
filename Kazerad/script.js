// Функция для извлечения параметров из URL
function getQueryParams() {
  const params = {};
  window.location.search.substr(1).split("&").forEach(function(item) {
    const [key, value] = item.split("=");
    params[key] = decodeURIComponent(value);
  });
  return params;
}

const queryParams = getQueryParams();
const chatFile = queryParams['chat'];
const errorContainer = document.getElementById('error-container');

if (chatFile) {
  fetch(chatFile)
    .then(response => response.json())
    .then(data => {
      // Сортировка сообщений по дате (от старых к новым)
      data.sort((a, b) => new Date(a.d) - new Date(b.d));
      
      const chatContainer = document.getElementById('chat-container');
      data.forEach(message => {
        const chatMessage = document.createElement('div');
        chatMessage.classList.add('message');
        chatMessage.innerHTML = `
          <div class="avatar">
          <img src="https://images.picarto.tv/${message.i}" alt="Avatar">
        </div>
        <div class="message-content">
          <span style="color: #${message.k};">${message.n}</span>${message.m}
          <div class="message-date">${new Date(message.d).toLocaleString()}</div>
        </div>
        `;
        chatContainer.appendChild(chatMessage);
      });
    })
    .catch(error => {
                    console.error('Error fetching data:', error);
                    errorContainer.innerText = `Error fetching the chat file: ${error.message}`;
                });
} else {
  errorContainer.innerText = 'No chat file specified in the URL';
}
