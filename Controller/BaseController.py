#! encoding: utf-8

from ast import Dict
import tornado.web
import json


class BaseController(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super(BaseController, self).__init__(application, request, **kwargs)


    def to_respond(self, code: int, status: str, data: Dict):
        to_json = { "code" : code, "status" : status, "data": data }
        self.write(to_json)
        self.finish()
 


    def setSecureCookie(self, name, value):
        self.set_secure_cookie(name, str(value))

    def getSecurecookie(self, name):
        return self.get_secure_cookie(name)

    def clearCookie(self, name):
        return self.clear_cookie(name)


    def get_current_request_url(self):
        current_full_url = "https://" + self.request.host + self.request.uri
        return current_full_url
        

    def get_client_ip(self):
        x_real_ip = self.request.headers.get("X-Real-IP")
        remote_ip = x_real_ip or self.request.remote_ip
        return remote_ip

        
    def is_wechat(self):
        if (self.is_mobile() or self.is_ipad()) and "MicroMessenger" in self.get_user_agent():
            return True
        return False


    def is_alipay(self):
        if (self.is_mobile() or self.is_ipad()) and "AlipayClient" in self.get_user_agent():
            return True
        return False
        

    def is_mobile(self):
        if self.is_iphone() or self.is_android():
            return True
        return False

    def is_iphone(self):
        if "iPhone" in self.get_user_agent():
            return True
        return False

    def is_android(self):
        if "Android" in self.get_user_agent():
            return True
        return False

    def is_ipad(self):
        if "iPad" in self.get_user_agent():
            return True
        return False

    def get_user_agent(self):
        user_agent = self.request.headers["User-Agent"]
        return user_agent

    
    def js_alert(self, msg):
        self.write("<script>alert('" + msg + "');</script>")
        self.finish()




