"""Garage client
Runs on device that interfaces with garage door opener

Main functions are to submit webcam images to server and respond
to commands from server
"""

import os
from datetime import datetime

import PIL.Image

from urllib3 import filepost
from urllib3.fields import RequestField

from tornado import httpclient, gen, options
from tornado.ioloop import IOLoop
from tornado.log import gen_log
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.httputil import HTTPHeaders
from tornado.options import define, options

from services.stamp import stamp
from services.image import image_to_stream


define("capture_interval", default=10, type=float)


BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def rel(path):
    return os.path.abspath(os.path.join(BASE, path))


conf_path = rel('client.conf')


# Time stamp format
format = '%Y-%M-%D %I:%M:%S %p'

def timestamp(img):
    now = datetime.now().strftime(format)
    stamp(img, (10, 10), str(now), size=20, fill='red')

    return img


def multipart(name, data, content_type='image/jpeg'):
    """Encode data as multipart form

    data will be encoded as form file field with name and filename
    equal to `name`

    returns tuple of (encoded body, content type)
    """

    fields = {
        name: (name, data, content_type)
    }

    encoded = filepost.encode_multipart_formdata(fields)

    return encoded


def post_data(url, name, data, content_type):
    """POST data to url encoded as multipart form"""

    encoded = multipart(name, data, content_type)

    body = encoded[0]
    content_type = encoded[1]

    headers = HTTPHeaders(
        {'content-type': content_type,
         'content-length': len(body)})

    client = AsyncHTTPClient()

    return client.fetch(
        HTTPRequest(url=url,
                    method='POST',
                    headers=headers,
                    body=body))


@gen.coroutine
def main():

    frame = PIL.Image.open('assets/test.jpg').convert(mode='RGB')

    while True:

        # start timer
        nxt = gen.sleep(options.capture_interval)

        stamped = timestamp(frame.copy())
        stream = image_to_stream(stamped)

        try:
            response = yield post_data(
                'http://localhost:8888/upload',
                'image_capture',
                stream.getvalue(),
                'image/jpeg')

        except Exception as ex:
            gen_log.error(ex)

        yield nxt


if __name__ == '__main__':
    options.parse_config_file(conf_path, final=False)
    options.parse_command_line()

    IOLoop.current().run_sync(main)
