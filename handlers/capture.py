import tornado.gen as gen
import tornado.web
import tornado.websocket
from tornado.options import define, options
from tornado.log import gen_log

from . import base
from services import auth


def nocache(handler):
    handler.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
    handler.set_header('Expires', 0)


class CaptureHandler(base.BaseHandler):
    def initialize(self, image_manager):
        self.image_manager = image_manager

    @gen.coroutine
    @tornado.web.authenticated
    def get(self):
        stream = self.image_manager.frame

        if stream is None:
            # Report error and end response
            self.set_status(503)
            return

        self.set_header('Content-Type', 'image/jpeg')
        self.set_header('Content-Length', len(stream.getbuffer()))

        nocache(self)

        for chunk in self.chunk_content(stream):
            try:
                self.write(chunk)
                yield self.flush()
            except tornado.iostream.StreamClosedError:
                return

    def chunk_content(self, stream):
        remaining = None
        stream.seek(0)
        while True:
            chunk_size = 64 * 1024
            if remaining is not None and remaining < chunk_size:
                chunk_size = remaining
            chunk = stream.read(chunk_size)
            if chunk:
                if remaining is not None:
                    remaining -= len(chunk)
                yield chunk
            else:
                if remaining is not None:
                    assert remaining == 0
                return

    def get_content(self, path):

        remaining = None

        with open(path, "rb") as file:
            while True:
                chunk_size = 64 * 1024
                if remaining is not None and remaining < chunk_size:
                    chunk_size = remaining
                chunk = file.read(chunk_size)
                if chunk:
                    if remaining is not None:
                        remaining -= len(chunk)
                    yield chunk
                else:
                    if remaining is not None:
                        assert remaining == 0
                    return


class CaptureSocketHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, image_manager):
        self.image_manager = image_manager

    def get_current_user(self):
        user_id = self.get_secure_cookie("garage_user")

        if not user_id:
            return None

        return auth.get_username(user_id)

    @gen.coroutine
    def open(self):
        # Authenticate user
        if (self.get_current_user() is None):
            self.close()
            return

        yield self.wait_on_capture()

    def on_message(self, message):
        pass

    @gen.coroutine
    def wait_on_capture(self):
        while True:
            yield self.image_manager.ready.wait()
            try:
                self.write_message('New capture available')
                gen_log.info('Notified client on websocket')
            except:
                return

    def on_close(self):
        print('Websocket closed')
