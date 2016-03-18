import tornado.web

import auth

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   'Password: <input type="password" name="password">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        username = self.get_argument('name')
        password = self.get_argument('password')

        if auth.authenticate(username, password):
            user_id = auth.get_user_id(username).bytes
            self.set_secure_cookie(
                'garage_user',
                user_id
            )

            self.redirect('/')
        else:
            self.redirect('/login')

class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie('garage_user')
        self.redirect('/')
