// scripts.js
var ws = new WebSocket("ws://localhost:8000/ws");

ws.onmessage = function(event) {
    var messages = document.getElementById('messages');
    var message = document.createElement('li');
    var content = document.createTextNode(event.data);
    message.className = 'received';
    message.appendChild(content);
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
};

function sendMessage(event) {
    var input = document.getElementById("messageText");
    if (input.value) {
        var messages = document.getElementById('messages');
        var message = document.createElement('li');
        var content = document.createTextNode(input.value);
        message.className = 'sent';
        message.appendChild(content);
        messages.appendChild(message);

        ws.send(input.value);
        input.value = '';
        messages.scrollTop = messages.scrollHeight;
    }
    event.preventDefault();
}

