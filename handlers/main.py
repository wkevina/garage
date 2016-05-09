import tornado.web

from . import base

class MainHandler(base.BaseHandler):
    """Render index.html"""
    @tornado.web.authenticated
    def get(self):
        self.render('index.html')
