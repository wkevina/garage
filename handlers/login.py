import tornado.web

from services import auth

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')


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
