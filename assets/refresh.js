import AutoSocket from 'autosocket.js';

function startRefresh() {
    console.log('load');
    var imgId = 'capture',
        as = new AutoSocket('/socket');

    as.on('message', function() {
        loadImage('/capture/?' + new Date().getTime()).
            then(function(newImg) {
                var oldImg = document.getElementById(imgId);
                oldImg.src = newImg.src;
            });
    });
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

if (document.readyState !== 'complete') {
    window.addEventListener('DOMContentLoaded', startRefresh);
} else {
    startRefresh();
}
