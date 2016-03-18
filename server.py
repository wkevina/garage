import os

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options

import capture
import auth
import login

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("garage_user")

        if not user_id:
            return None

        return auth.get_username(user_id)

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write('Hey guys!')

static_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'assets')
)

settings = dict(
    debug=True,
    autoreload=True,
    cookie_secret=os.urandom(32),
    login_url='/login'
)

routes = [
    (r"/capture/", capture.CaptureHandler),
    (r"/(.*\.(html|js|jsx|css|png|jpg|jpeg))", tornado.web.StaticFileHandler,
     dict(path=static_path)
    ),
    ('/', MainHandler),
    ('/login', login.LoginHandler),
    ('/logout', login.LogoutHandler),
    # ('.*', tornado.web.FallbackHandler)
]

def main():
    tornado.options.parse_command_line()

    print("Launching server with settings:\n")
    print(settings)

    auth.add_user('root', 'root')

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
