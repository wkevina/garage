window.addEventListener('load', function() {

    var imgId = 'capture',
        host = window.location.host,
        protocol = window.location.protocol,
        wsProtocol;

    if (protocol == 'http:') {
        wsProtocol = 'ws://';
    } else if (protocol == 'https:') {
        wsProtocol = 'wss://';
    }

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

    var captureImg = document.getElementById(imgId);

    function openSocket() {
        return new WebSocket(wsProtocol + host + '/socket');
    }


    if (captureImg !== null) {
        var ws;

        function connectSocket() {
            try {
                ws = openSocket();

                ws.addEventListener('open', function(evt) {
                    ws.addEventListener('message', function(evt) {
                        loadImage('/capture/?' + new Date().getTime()).
                            then(function(newImg) {
                                var oldImg = document.getElementById(imgId);
                                oldImg.src = newImg.src;
                            });
                    });

                    window.addEventListener('unload', function() {
                        ws.close();
                    });
                });

                ws.addEventListener('close', function(evt) {
                    window.setTimeout(checkConnection, 1000);
                });
            } catch (ex) {
                window.setTimeout(checkConnection, 1000);
            }
        }

        function checkConnection() {
            if (ws && ws.readyState != WebSocket.OPEN) {
                connectSocket();
            }
        }

        connectSocket();
        window.setTimeout(checkConnection, 1000);
    }
});
