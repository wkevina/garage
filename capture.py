import datetime
import io

import PIL.Image
import tornado.gen as gen
import tornado.web
import tornado.websocket
import tornado.locks
import tornado.concurrent

import stamp

_current_frame = None

condition = tornado.locks.Condition()

@gen.coroutine
def capture():
    # Placeholder implementation
    # Will call cam.capture eventually
    frame = PIL.Image.new("RGB", (640, 480))

    return frame

@gen.coroutine
def timestamp(img):
    now = datetime.datetime.now()

    stamp.stamp(img, (10, 10), str(now), size=20)

    return img

@gen.coroutine
def image_to_stream(img, format="JPEG"):
    stream = io.BytesIO()
    img.save(stream, format=format)

    return stream

def current_frame():
    return _current_frame

def set_frame(frame):
    global _current_frame
    _current_frame = frame

@gen.coroutine
def task():
    i = 1
    while True:
        nxt = gen.sleep(2.5)
        print('capture.task')

        cap = yield capture()

        yield timestamp(cap)

        frame = yield image_to_stream(cap)
        set_frame(frame)

        assert frame is _current_frame

        condition.notify_all()

        yield nxt


class CaptureHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.set_header('Content-Type', 'image/jpeg')

        stream = current_frame()

        self.set_header("Content-Length", len(stream.getbuffer()))

        for chunk in self.chunk_content(stream):
            print("Writing chunk")
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
    @gen.coroutine
    def open(self):
        self._start_future = tornado.concurrent.Future()
        yield self.wait_on_capture()

    def on_message(self, message):
        self.write_message('You said: ' + message)
        self._start_future.set_result(None)

    @gen.coroutine
    def wait_on_capture(self):
        yield self._start_future
        while True:
            yield condition.wait()
            try:
                self.write_message('New capture available')
            except:
                return

    def on_close(self):
        print('Websocket closed')
