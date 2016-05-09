import Emitter from 'component/emitter';

export class AutoSocket {
    constructor(path) {
        this.path = path;
        this.socket = null;
        this.timeout = null;

        this.onOpen = this.onOpen.bind(this);
        this.onClose = this.onClose.bind(this);
        this.onError = this.onError.bind(this);
        this.onMessage = this.onMessage.bind(this);

        this.connect();
    }

    connect() {
        if (!this.socket) {
            const socket = new WebSocket(this.getUri());
            this.socket = socket;
            this.socket.addEventListener('open', this.onOpen);
            this.socket.addEventListener('close', this.onClose);
            this.socket.addEventListener('error', this.onError);
            this.socket.addEventListener('message', this.onMessage);
        }

        this.timeout = window.setTimeout(this.reconnect.bind(this), 5000);
    };

    reconnect() {
        this.timeout = null;
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
        this.connect();
    };

    getUri() {
        const host = window.location.host,
              protocol = this.getProtocol();

        let uri = '';

        uri += protocol;
        uri += '//';
        uri += host;
        uri += this.path;

        return uri;
    };

    getProtocol() {
        let protocol = window.location.protocol;

        if (protocol == 'http:') {
            return 'ws:';
        } else if (protocol == 'https:') {
            return 'wss:';
        } else {
            console.log(
                "I don't know how this could happen. What kind of protocol is " +
                    protocol + "?"
            );
            return 'ws:';
        }
    };

    onOpen() {
        if (this.timeout) {
            window.clearTimeout(this.timeout);
            this.timeout = null;
        }
        // Emit event to subscribers
        this.emit('open');
    };
    onClose() {
        if (!this.timeout) {
            this.reconnect();
        }
        // Emit event to subscribers
        this.emit('close');
    };

    onError() {
        // Emit event to subscribers
        this.emit('error');
    };

    onMessage(msg) {
        // Emit event to subscribers
        this.emit('message', msg);
    };

    send(msg) {
        // Submit data to socket
        if (this.socket && this.socket.readyState == WebSocket.OPEN) {
            this.socket.send(msg);
        }
    };
}

// Mixin Emitter
Emitter(AutoSocket.prototype);

export default AutoSocket;
