from tornado.web import HTTPError

from .base import BaseHandler

FILENAME = 'image_capture'

class UploadHandler(BaseHandler):
    def initialize(self, image_manager):
        self.image_manager = image_manager

    def post(self):

        files = self.request.files

        if FILENAME in files:
            file_info = files[FILENAME][0]
            content_type = file_info['content_type']
            data = file_info['body']

            if content_type != 'image/jpeg':
                msg = 'Client submitted image is not image/jpeg data'
                raise HTTPError(415, msg)

            self.image_manager.update_frame(data)

            self.set_status(200)

        else:
            msg = "Request does not include {} form field".format(FILENAME)
            raise HTTPError(400, msg)
