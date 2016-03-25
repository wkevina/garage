window.addEventListener('load', function() {
    var imgId = 'capture',
        as = new AutoSocket('/socket');

    as.on('message', function() {
        loadImage('/capture/?' + new Date().getTime()).
            then(function(newImg) {
                var oldImg = document.getElementById(imgId);
                oldImg.src = newImg.src;
            });
    });
});

function loadImage(url) {
    var newImg = new Image(),
        deferred = new Promise(function (resolve, reject) {
            newImg.src = url;

            newImg.addEventListener('load', function() {
                resolve(newImg);
            });

            newImg.addEventListener('error', function() {
                reject(newImg);
            });

            newImg.addEventListener('abort', function() {
                reject(newImg);
            });
        });

    return deferred;
}

function AutoSocket(path) {
    this.path = path;
    this.socket = null;
    this.timeout = null;

    this.onOpen = this.onOpen.bind(this);
    this.onClose = this.onClose.bind(this);
    this.onError = this.onError.bind(this);
    this.onMessage = this.onMessage.bind(this);

    this.connect();
}

AutoSocket.prototype.connect = function() {
    if (!this.socket) {
        var socket = new WebSocket(this.getUri());
        this.socket = socket;
        this.socket.addEventListener('open', this.onOpen);
        this.socket.addEventListener('close', this.onClose);
        this.socket.addEventListener('error', this.onError);
        this.socket.addEventListener('message', this.onMessage);
    }

    this.timeout = window.setTimeout(this.reconnect.bind(this), 5000);
};

AutoSocket.prototype.reconnect = function() {
    this.timeout = null;
    if (this.socket) {
        this.socket.close();
        this.socket = null;
    }
    this.connect();
};

AutoSocket.prototype.getUri = function() {
    var host = window.location.host,
        protocol = this.getProtocol(),
        uri = '';

    uri += protocol;
    uri += '//';
    uri += host;
    uri += this.path;

    return uri;
};

AutoSocket.prototype.getProtocol = function() {
    var protocol = window.location.protocol;

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

AutoSocket.prototype.onOpen = function() {
    if (this.timeout) {
        window.clearTimeout(this.timeout);
        this.timeout = null;
    }
    // Emit event to subscribers
    this.emit('open');
};

AutoSocket.prototype.onClose = function() {
    if (!this.timeout) {
        this.reconnect();
    }
    // Emit event to subscribers
    this.emit('close');
};

AutoSocket.prototype.onError = function() {
    // Emit event to subscribers
    this.emit('error');
};

AutoSocket.prototype.onMessage = function(msg) {
    // Emit event to subscribers
    this.emit('message', msg);
};

AutoSocket.prototype.send = function(msg) {
    // Submit data to socket
    if (this.socket && this.socket.readyState == WebSocket.OPEN) {
        this.socket.send(msg);
    }
};

// Mixin Emitter
Emitter(AutoSocket.prototype);
