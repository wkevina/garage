$(function() {

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
        var newImg = $('<img>'),
            promise = newImg.load()
                .promise()
                .done(function() {
                    return newImg;
                });

        newImg.attr('src', url);

        return promise;
    }

    var ws = new WebSocket(wsProtocol + host + '/socket');

    ws.onopen = function() {
        ws.send("Hey, I'm Firefox.");
    };

    ws.onmessage = function(evt) {
        loadImage('/capture/?' + new Date().getTime()).
            done(function(newImg) {
                var oldImg = $('#' + imgId);

                oldImg.replaceWith(newImg);

                newImg.attr('id', imgId);
            });
    };

    $(window).on("unload", function() {
        ws.close();
    });

});
