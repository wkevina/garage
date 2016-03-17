import os

import tornado.ioloop
import tornado.web
import tornado.httpserver


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hey guys!')


static_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'assets')
)

settings = dict(
    debug=True,
    autoreload=True
)

routes = [
     (r"/(.*\.(html|js|jsx|css|png|jpg|jpeg))", tornado.web.StaticFileHandler,
      dict(path=static_path)
     ),
    ('/', MainHandler),
    # ('.*', tornado.web.FallbackHandler)
]

if __name__ == '__main__':
    print("Launching server with settings:\n")
    print(settings)

    application = tornado.web.Application(
        routes,
        **settings
    )

    server = tornado.httpserver.HTTPServer(application)
    server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
