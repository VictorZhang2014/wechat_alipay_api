#! encoding: utf-8

import json, time, datetime, random, string, urllib3
from Controller.BaseController import BaseController
from Utility.HashUtils import HashUtils
from xml.etree import ElementTree


class WXPayController(BaseController):

    # 统一下单：https://pay.weixin.qq.com/wiki/doc/api/H5.php?chapter=9_20&index=1
    # 签名方式：https://pay.weixin.qq.com/wiki/doc/api/H5.php?chapter=4_3

    def __init__(self, application, request, **kwargs):
        super(WXPayController, self).__init__(application, request, **kwargs)
        self.merchant_id = ""
        self.app_id = ""
        self.app_secret = "" 


    def post(self):
        _data = json.loads(self.request.body)
        
        openid = _data.get("openid")
        if openid is None or len(openid) == 0:
            self.to_respond(-1, "openid不能为空", {})
            return

        amount = _data.get("total_amount")
        if amount is None:
            amount = 0
        if isinstance(amount, str):
            amount = int(amount)

        subject = _data.get("subject")
        if subject is None or len(subject) == 0:
            subject = "用户充值"

        remote_ip = _data.get("remote_ip")
        if remote_ip is None or len(remote_ip) == 0:
            remote_ip = "47.94.0.5" # "127.0.0.1"

        notify_url = _data.get("notify_url")
        if notify_url is None or len(notify_url) == 0:
            notify_url = "https://pay.google.com/api/pay/wxpay/notify/2ZVdsRgSRuagrHktg6Csx8yR5xACsB1PpiFJvzJs"

        out_trade_no = HashUtils.md5(HashUtils.uuid()) 

        success, data = self._create_unified_order(out_trade_no, subject, amount, remote_ip, openid, notify_url)
        if not success:
            self.to_respond(-1, data, {})
            return

        self.to_respond(0, "success", data)


    def _create_unified_order(self, order_no, subject, total_fee, spbill_create_ip, openid, notify_url):
        """
        统一下单
        https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1
        """ 
        # time_start = self.getDateTimeUnionStr()
        # time_expire = self.getDateTimeUnionStr(minutes=30) 
        sign_type = "MD5"
        nonce_str = self.get_nonce_str()
        parameters = {
            "appid" : self.app_id,  
            "mch_id" : self.merchant_id,  
            "device_info" : "MWEB",
            "nonce_str" : nonce_str,
            # "sign" : "",
            "sign_type" : sign_type,
            "body" : subject, 
            # "detail" : "",
            "out_trade_no" : order_no,
            "fee_type" : "CNY",
            "total_fee" : total_fee,
            "spbill_create_ip" : spbill_create_ip,
            # "time_start" : time_start,
            # "time_expire" : time_expire,
            # "goods_tag" : "",
            "notify_url" : notify_url,
            "trade_type" : "JSAPI",
            "openid" : openid,
            # "receipt" : "",
            # "scene_info" : ""
        }
        # 生成签名，签名验证工具https://pay.weixin.qq.com/wiki/tools/signverify/
        parameters["sign"] = self.generate_signature(parameters)
        print(parameters)

        # 构建xml格式的参数
        xml_parameters = "<xml>"
        for key, value in parameters.items():
            xml_parameters += "<{}>{}</{}>".format(key, value, key)
        xml_parameters += "</xml>"
        print(xml_parameters)
    
        # 请求接口
        general_url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        resp_data = self.request_with_url(general_url, parameters=xml_parameters.encode("utf-8"))

        # 解析XML
        returned_dict = {}
        for child in ElementTree.fromstring(resp_data):
            returned_dict[child.tag] = child.text

        if "result_code" in returned_dict.keys() and returned_dict["result_code"] == "SUCCESS":
            wxpay_param = self.generate_jssdk_signature(parameters["appid"], nonce_str, returned_dict["prepay_id"], sign_type, order_no)
            wxpay_param["sign"] = parameters["sign"]
            return True, wxpay_param
        else:
            err_code_des = ""
            if "err_code_des" in returned_dict.keys():
                err_code_des = returned_dict["err_code_des"]
            elif "return_msg" in returned_dict.keys():
                err_code_des = returned_dict["return_msg"]
            return False, err_code_des


    def generate_jssdk_signature(self, appid, nonce_str, prepay_id, sign_type, order_No):
        # 生成JSAPI调起支付所需的签名
        timeStamp = int(time.time())
        wxpay_param = {
            "appId" : appid,  
            "timeStamp" : str(timeStamp),
            "nonceStr" : nonce_str,
            "package" : "prepay_id=" + prepay_id,
            "signType" : sign_type,
        }
        wxpay_param["paySign"] = self.generate_signature(wxpay_param)
        wxpay_param["out_trade_no"] = order_No
        wxpay_param["prepay_id"] = prepay_id
        return wxpay_param


    def get_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))


    def generate_xml_params(self, parameters):
        """
        构建xml格式的参数
        """
        xml_parameters = "<xml>"
        for key, value in parameters.items():
            xml_parameters += "<{}>{}</{}>".format(key, value, key)
        xml_parameters += "</xml>"
        return xml_parameters


    def generate_signature(self, parameters):
        unsinged_str = '&'.join(['{}={}'.format(key, parameters[key]) for key in sorted(parameters)])
        unsinged_str += "&key=" + self.app_secret
        return HashUtils.md5(unsinged_str).upper() 


    def getDateTimeUnionStr(self, minutes=0):
        '''
        当前时间
        :return: 以格式'%Y%m%d%H%M%S'返回
        '''
        if minutes == 0:
            local = time.localtime()
            return time.strftime('%Y%m%d%H%M%S', local)
        else:
            more_hours = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
            return "{:%Y%m%d%H%M%S}".format(more_hours)


    def request_with_url(self, url_str, method="POST", parameters=None):
        """
        https://urllib3.readthedocs.io/en/latest/user-guide.html
        """
        http = urllib3.PoolManager()
        response = http.request(method,
                                url_str, 
                                headers={ 
                                    'Content-Type' : 'application/xml' 
                                },
                                body=parameters)
        resp_xml = str(response.data, encoding="utf-8")
        return resp_xml
