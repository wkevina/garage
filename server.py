import os

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from tornado.options import define, options

import capture
import auth
import login

define('server_port', default=8888, type=int)
define('server_hostname', default='localhost', type=str)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("garage_user")

        if not user_id:
            return None

        return auth.get_username(user_id)

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('base.html')

def rel(path):
    return os.path.abspath(
    os.path.join(os.path.dirname(__file__), path)
)

static_path = rel('assets')
template_path = rel('templates')
conf_path = rel('garage.conf')

settings = dict(
    debug=True,
    autoreload=True,
    cookie_secret=os.urandom(32),
    login_url='/login',
    static_path=static_path,
    template_path=template_path
)

routes = [
    (r"/capture/", capture.CaptureHandler),
    ('/', MainHandler),
    ('/login', login.LoginHandler),
    ('/logout', login.LogoutHandler),

]

def main():
    tornado.options.parse_config_file(conf_path, final=False)
    tornado.options.parse_command_line()

#    auth.install_admin()

    application = tornado.web.Application(
        routes,
        **settings
    )

    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.server_port)

    tornado.ioloop.IOLoop.current().run_sync(capture.task)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
