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

    if (captureImg !== null) {
        var ws = new WebSocket(wsProtocol + host + '/socket');

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
    }
});
