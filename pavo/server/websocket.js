let ws = new WebSocket("ws://127.0.0.1:5556/ws");
ws.onopen = function() {
    ws.send('Connected!');
}

ws.onmessage = function (e) {
    window.location.reload(true);
}