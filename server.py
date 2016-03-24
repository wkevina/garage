import os
import sys

import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.log import gen_log
import tornado.options
from tornado.options import define, options

import basehandler
import capture
import auth
import login
import config

define('server_port', default=8888, type=int)
define('server_hostname', default='localhost', type=str)

class MainHandler(basehandler.BaseHandler):
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
persistent_path = rel('storage.db')

settings = dict(
    debug=True,
    autoreload=True,
    login_url='/login',
    static_path=static_path,
    template_path=template_path
)

routes = [
    (r"/capture/", capture.CaptureHandler),
    (r"/socket", capture.CaptureSocketHandler),
    ('/', MainHandler),
    ('/login', login.LoginHandler),
    ('/logout', login.LogoutHandler),
]

def main():
    config.init(persistent_path)

    tornado.options.parse_config_file(conf_path, final=False)
    tornado.options.parse_command_line()

    key = config.get_option('cookie_secret')
    if key is None:
        gen_log.error('Fatal: secret key not found. '
                          'Run `manage.py keys` to create it')
        sys.exit()

    settings['cookie_secret'] = key

    auth.init()

    application = tornado.web.Application(
        routes,
        **settings
    )

    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.server_port)

    tornado.ioloop.IOLoop.current().spawn_callback(capture.task)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
