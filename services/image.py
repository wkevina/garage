from io import BytesIO

from tornado.locks import Condition
from . import stamp

class ImageManager():
    def __init__(self):
        # Image data
        self._frame = None
        # Flow control
        self._condition = Condition()

    def timestamp(self, img):
        now = datetime.datetime.now()
        stamp.stamp(img, (10, 10), str(now), size=20)

        return img

    def update_frame(self, frame):
        self._frame = BytesIO(frame)
        self.ready = True

    @property
    def frame(self):
        return self._frame

    @property
    def ready(self):
        return self._condition

    @ready.setter
    def ready(self, cond):
        if cond is True:
            self._condition.notify_all()


def image_to_stream(img, format="JPEG"):
    """Convert PIL image to encoded byte stream"""
    stream = BytesIO()
    img.save(stream, format=format)

    return stream
