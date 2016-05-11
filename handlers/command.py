from datetime import datetime

import tornado.web

from . import base

q = []

q.append(dict(code=0, time=datetime.now().isoformat()))

class CommandHandler(base.BaseHandler):
    """Handles command queue data"""
    def get(self):
        self.write(dict(queue=q))
