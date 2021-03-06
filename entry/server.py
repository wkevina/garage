import os
import sys

import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.log import gen_log
import tornado.options
from tornado.options import define, options

from handlers import main, capture, upload, login, command
from services import auth, config, image

define('server_port', default=8888, type=int)
define('server_hostname', default='localhost', type=str)

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def rel(path):
    return os.path.abspath(os.path.join(BASE, path))

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

# Shared image manager
# Used to synchronize capturing of new frames with serving that data
image_manager = image.ImageManager()

routes = [
    ('/capture/', capture.CaptureHandler, dict(image_manager=image_manager)),
    ('/upload', upload.UploadHandler, dict(image_manager=image_manager)),
    ('/socket', capture.CaptureSocketHandler, dict(image_manager=image_manager)),
    ('/command', command.CommandHandler),
    ('/', main.MainHandler),
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

    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
