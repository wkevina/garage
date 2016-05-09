import tornado.web

from . import basehandler

class MainHandler(basehandler.BaseHandler):
    """Render index.html"""
    @tornado.web.authenticated
    def get(self):
        self.render('index.html')
