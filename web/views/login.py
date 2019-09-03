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
        name = self.get_argument("name") # 获取用户名
        # 用户信息列表
        edroity_name_list = {'jiangjunnan': 'xijunnan', 'wupeng': 'Edroity4000', 'chenjialu': 'Edroity4000', 'wangjun': 'Edroity4000', 'liuqianjun': 'Edroity4000', 'jianghong': 'Edroity4000', 'qianzaiyi': 'Edroity4000', 'huangxiang': 'Edroity4000', 'yangyibin': 'Edroity4000', 'zuoyongbo': 'Edroity4000', 'chenyukuan': 'Edroity4000', 'yaozhenggang': 'Edroity4000', 'pengzhiyuan': 'Edroity4000', 'zhaolei': 'Edroity4000', 'huangguanjie': 'Edroity4000', 'songtiefei': 'Edroity4000', 'sunxiaofei': 'Edroity4000', 'huangwanchao': 'Edroity4000', 'zhangyun': 'Edroity4000'}
        password = self.get_argument("password")
        
        
        if name in edroity_name_list.keys():
            if password == edroity_name_list[name]:
                email = name + "@edroity.com"
                await self.set_current_user(email, name)
                next_url = self.get_cookie("next", "/")
                self.clear_cookie("next")
                self.redirect(next_url)
            else:
                self.write('<html><body>Wrong Password!</body></html>')
        else:
            self.write('<html><body>You are not in Edroity.</body></html>')
