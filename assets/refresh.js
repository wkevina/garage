import AutoSocket from 'autosocket.js';

function startRefresh() {
    console.log('load');
    const imgId = 'capture',
          as = new AutoSocket('/socket');

    as.on('message', function() {
        loadImage('/capture/?' + new Date().getTime()).
            then(function(newImg) {
                requestAnimationFrame(function() {
                    const oldImg = document.getElementById(imgId);
                    oldImg.src = newImg.src;
                    console.log(oldImg.attributes);
                });
            });
    });
}

function loadImage(url) {
    const newImg = new Image(),
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
