import tornado.ioloop
import os

from Controller.IndexController import IndexController
from Controller.AliPayController import AliPayController
# from Controller.AliPayNotifyUrlController import AliPayNotifyUrlController
from Controller.WXPayController import WXPayController


from tornado.options import define, options
define("port", default=9123, help="run on the given port", type=int)



class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", IndexController),
            (r"/api/alipay/order", AliPayController),
            # (r"/api/alipay/notify", AliPayNotifyUrlController),
            (r"/api/wxpay/prepay", WXPayController)
        ]
        settings = dict(
            # template_path=os.path.join(os.path.dirname(__file__), "templates"),
            # static_path=os.path.join(os.path.dirname(__file__), "static"), 
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.current().start()



if __name__ == "__main__":
    main()


