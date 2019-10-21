import tornado.web
from utils.account import authenticate, register
from .main import BaseHandler


class RegisterHandler(BaseHandler):
    def get(self):
        self.render('register.html')

    def post(self):
        username = self.get_argument('username', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')

        if username and password1 and (password1 == password2):
            register(username, password1)
            self.session.set('tudo_user', username)
            self.redirect('/')
        else:
            self.write('bad username/password')


class LoginHandler(BaseHandler):
    def get(self):
        next_url = self.get_argument('next', '')
        msg = self.get_argument('msg', '')
        self.render('login.html', next_url=next_url, msg=msg)

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        next_url = self.get_argument('next', '')

        if not username.strip() or not password.strip():
            self.redirect('/login?msg=empty password or username')
        else:
            if authenticate(username, password):
                self.session.set('tudo_user', username)     # 设置session
                if next_url:
                    self.redirect(next_url)
                else:
                    self.redirect('/')
            else:
                self.redirect('/login?msg=password error')


class LogoutHandler(BaseHandler):
    def get(self):
        self.session.delete("tudo_user")
        self.render('logout.html')


