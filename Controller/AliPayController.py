#! encoding: utf-8

import json, urllib3
from Controller.BaseController import BaseController
from Controller.CertificateManager import CertificateManager
from Utility.HashUtils import HashUtils

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient

from alipay.aop.api.domain.AlipayTradeWapPayModel import AlipayTradeWapPayModel
from alipay.aop.api.request.AlipayTradeWapPayRequest import AlipayTradeWapPayRequest

from alipay.aop.api.domain.AlipayTradeQueryModel import AlipayTradeQueryModel
from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest


class AliPayController(BaseController):
    
    # 技术文档：https://opendocs.alipay.com/open/repo-0038v7

    def __init__(self, application, request, **kwargs):
        super(AliPayController, self).__init__(application, request, **kwargs)
        self.ALIPAY_APP_ID = "" # 指南针彩经
        self.NOTIFY_URL = "https://pay.google.com/api/pay/alipay/notify/XQY7Vr5f9EKhiXXPoK9mGphPsGLtiYcQBGtpD6pa"


    def post(self):
        _data = json.loads(self.request.body)
        
        total_amount = _data.get("total_amount")
        if total_amount is None or total_amount == 0 or len(total_amount) == 0:
            subject = "0"

        subject = _data.get("subject")
        if subject is None or len(subject) == 0:
            subject = "指南针彩经"

        body = _data.get("body")
        if body is None or len(body) == 0:
            body = "指南针彩经"

        notify_url = _data.get("notify_url")
        if notify_url is None or len(notify_url) == 0:
            notify_url = self.NOTIFY_URL

        alipay_client_config = AlipayClientConfig() 
        alipay_client_config.app_id = self.ALIPAY_APP_ID
        alipay_client_config.alipay_public_key = CertificateManager.readAliPayPublicKey()
        alipay_client_config.app_private_key = CertificateManager.readAliPayPrivateKey()

        out_trade_no = self.get_out_order_no()

        model = AlipayTradeWapPayModel()
        model.out_trade_no = out_trade_no
        model.total_amount = total_amount
        model.subject = subject
        model.body = body
        model.product_code = "QUICK_WAP_WAY"
        
        alipay_request = AlipayTradeWapPayRequest(biz_model=model)
        alipay_request.notify_url = notify_url

        client = DefaultAlipayClient(alipay_client_config=alipay_client_config)
        try:
            response_url = client.page_execute(alipay_request, http_method="GET")
            self.to_respond(0, "success", {"out_trade_no": out_trade_no, "pay_url": response_url})
        except Exception as e:
            self.to_respond(-1, str(e), {})


    def get_out_order_no(self) -> str:
        """
        生成订单号
        商户系统内部订单号，要求32个字符内，只能是数字、大小写字母_-|*@ ，且在同一个商户号下唯一。
        """
        return HashUtils.md5(HashUtils.uuid())


    def put(self):
        _data = json.loads(self.request.body)
        
        out_trade_no = _data.get("out_trade_no")

        alipay_client_config = AlipayClientConfig() 
        alipay_client_config.app_id = self.ALIPAY_APP_ID
        alipay_client_config.alipay_public_key = CertificateManager.readAliPayPublicKey()
        alipay_client_config.app_private_key = CertificateManager.readAliPayPrivateKey()

        model = AlipayTradeQueryModel()
        model.out_trade_no = out_trade_no
        
        alipay_request = AlipayTradeQueryRequest(biz_model=model)

        client = DefaultAlipayClient(alipay_client_config=alipay_client_config)
        try: 
            response_url = client.page_execute(alipay_request, http_method="GET")

            http = urllib3.PoolManager()
            response = http.request("get", response_url, headers={ 'Content-Type' : 'application/json' })
            resp = json.loads(response.data)

            query_response = resp.get("alipay_trade_query_response")
            _code = query_response.get("code")
            _msg = query_response.get("msg")
            if int(_code) != 10000:
                self.to_respond(-1, "Code: {} Message: {}".format(_code, _msg), {})
                return
            _out_trade_no = query_response.get("out_trade_no")
            _total_amount = float(query_response.get("total_amount")) * 100 # 转换成单位：分
            _trade_status = query_response.get("trade_status") # TRADE_SUCCESS
            self.to_respond(0, "success", {"out_trade_no": _out_trade_no, "total_amount": _total_amount, "trade_status": _trade_status})
        except Exception as e:
            self.to_respond(-1, str(e), {})
