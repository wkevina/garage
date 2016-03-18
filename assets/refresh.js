cap = document.getElementById('capture');

ws = new WebSocket('ws://localhost:8888/socket');

ws.onopen = () => ws.send("Hey, I'm Firefox.");

ws.onmessage = (evt) => cap.src = '/capture/?' + new Date().getTime();
