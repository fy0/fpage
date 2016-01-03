# coding:utf-8

from view import route, url_for, View, LoginView, NoLoginView
from model.user import User


@route('/signin', name='signin')
class SignIn(NoLoginView):
    def get(self):
        self.render('user/signin.html')

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        remember = self.get_argument('remember', False)
        next = self.get_argument('next', None)

        error = False
        u = User.auth(username, password)
        if not u:
            error = True
            self.messages.error("帐号或密码错误！")

        if not error:
            self.messages.success("登陆成功！")
            expires = 30 if remember else None
            self.set_secure_cookie("u", u.key, expires_days=expires)
            if next:
                return self.redirect(next)
            return self.redirect(url_for("index"))

        self.render('user/signin.html')


@route('/signout', name='signout')
class SignOut(LoginView):
    def get(self):
        self.clear_cookie('u')
        self.messages.success("您已成功登出！")
        self.redirect(url_for("index"))


@route('/signup', name='signup')
class SignUp(NoLoginView):
    def get(self):
        self.render('user/signup.html')

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        password_again = self.get_argument("password_again")
        next = self.get_argument('next', None)

        error = False
        if not (3 <= len(username) <= 15):
            error = True
            self.messages.error("用户名长度必须在 3-15 之间")
        if len(password) < 3:
            error = True
            self.messages.error("密码长度必须大于等于3")
        if User.exist(username):
            error = True
            self.messages.error("用户已存在！")
        if password != password_again:
            error = True
            self.messages.error("两次输入的密码不一致！")

        if not error:
            u = User.new(username, password)
            self.messages.success("账户创建成功！")
            self.redirect(url_for('signin') + (('?next=%s' % next) if next else ''))
            return

        self.render('user/signup.html')
