"""Garage client
Runs on device that interfaces with garage door opener

Main functions are to submit webcam images to server and respond
to commands from server
"""

import io
import PIL.Image

from tornado import httpclient, gen, options
from tornado.ioloop import IOLoop
from tornado.log import gen_log
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


def image_to_stream(img, format="JPEG"):
    stream = io.BytesIO()
    img.save(stream, format=format)

    return stream

def multi_part(data, name='data'):
    buffer = io.BytesIO()


@gen.coroutine
def main():
    client = AsyncHTTPClient()
    while True:
        frame = PIL.Image.new("RGB", (20, 20))
        stream = image_to_stream(frame)
        try:
            response = yield client.fetch(
                HTTPRequest(
                    url='http://localhost:8888',
                    method='POST',
                    body=stream.getvalue()))

        except Exception as ex:
            gen_log.error(ex)
        else:
            print(response)
        yield gen.sleep(10)


if __name__ == '__main__':
    options.parse_command_line()

    IOLoop.current().run_sync(main)
