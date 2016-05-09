from .base import BaseHandler

class UploadHandler(BaseHandler):
    def get(self):
        self.write('UploadHandler')

    def post(self):
        print(self.request)
        #print(self.request.body)
        self.set_status(200)
