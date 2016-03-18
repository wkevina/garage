import os

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options

import capture

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
    (r"/capture/", capture.CaptureHandler),
    (r"/(.*\.(html|js|jsx|css|png|jpg|jpeg))", tornado.web.StaticFileHandler,
     dict(path=static_path)
    ),
    ('/', MainHandler),
    # ('.*', tornado.web.FallbackHandler)
]

def main():
    tornado.options.parse_command_line()

    print("Launching server with settings:\n")
    print(settings)

    application = tornado.web.Application(
        routes,
        **settings
    )

    server = tornado.httpserver.HTTPServer(application)
    server.listen(8888)

    tornado.ioloop.IOLoop.current().run_sync(capture.task)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
