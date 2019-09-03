# coding: utf-8
#
from logzero import logger

from .auth import AuthError, OpenIdMixin
from .base import BaseRequestHandler

from ..settings import AUTH_BACKENDS
# import hashlib

class OpenIdLoginHandler(BaseRequestHandler, OpenIdMixin):
    _OPENID_ENDPOINT = AUTH_BACKENDS['openid']['endpoint']

    async def get(self):
        if self.get_argument("openid.mode", False):
            try:
                user = await self.get_authenticated_user()
            except AuthError as e:
                self.write(
                    "<code>Auth error: {}</code> <a href='/login'>Login</a>".
                    format(e))
            else:
                logger.info("User info: %s", user)
                await self.set_current_user(user['email'], user['name'])
                next_url = self.get_argument('next', '/')
                self.redirect(next_url)
        else:
            self.authenticate_redirect()


class SimpleLoginHandler(BaseRequestHandler):
    def get(self):
        self.set_cookie("next", self.get_argument("next", "/"))
        self.render("login.html")


# pw = 'Edroity666' # 需要加密的字符串
# def md5Encode(str):
#     # 创建MD5对象
#     mdfive = hashlib.md5()
#     mdfive.update(str) # 传入需要加密的字符串进行MD5加密
#     return mdfive.hexdigest() # 获取到经过MD5加密的字符串返回
# npw = 'md5Encode(pw.encode('utf-8')')
# # 这里必须用encode()函数对字符串进行编码，不然会报 TypeError: Unicode-objects must be encoded before hashing
# print(npw)


    async def post(self):
        name = self.get_argument("name")
        password = self.get_argument("password")
        print(password)
        if password != 'Edroity666': # 默认密码
            self.write('<html><body>PASSWORD ERROR</body></html>')
        else:
            email = name + "@anonymous.com"
            await self.set_current_user(email, name)
            next_url = self.get_cookie("next", "/")
            self.clear_cookie("next")
            self.redirect(next_url)
