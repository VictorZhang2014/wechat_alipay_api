#! encoding: utf-8

from typing import Dict
import json
from Controller.BaseController import BaseController


class AliPayNotifyUrlController(BaseController):
    """
    支付宝手机网站支付结果异步通知
    官方文档：https://docs.open.alipay.com/203/105286/
    """

    def __init__(self, application, request, **kwargs):
        super(AliPayNotifyUrlController, self).__init__(application, request, **kwargs)


    def post(self):
        notify_time = self.get_argument("notify_time")
        notify_type = self.get_argument("notify_type", "")
        notify_id = self.get_argument("notify_id", "")
        subject = self.get_argument("subject")
        body = self.get_argument("body")
        app_id = self.get_argument("app_id")
        seller_id = self.get_argument("seller_id")
        seller_email = self.get_argument("seller_email")
        buyer_id = self.get_argument("buyer_id")
        auth_app_id = self.get_argument("auth_app_id")
        buyer_logon_id = self.get_argument("buyer_logon_id")
        fund_bill_list = self.get_argument("fund_bill_list")
        fund_bill_list = json.loads(fund_bill_list)
        fund_bill_list_account = fund_bill_list[0]["amount"]
        fund_bill_list_fundChannel = fund_bill_list[0]["fundChannel"]
        trade_status = self.get_argument("trade_status")
        total_amount = self.get_argument("total_amount")
        invoice_amount = self.get_argument("invoice_amount")
        receipt_amount = self.get_argument("receipt_amount")
        buyer_pay_amount = self.get_argument("buyer_pay_amount")
        point_amount = self.get_argument("point_amount")
        version = self.get_argument("version")
        out_trade_no = self.get_argument("out_trade_no")
        trade_no = self.get_argument("trade_no")
        charset = self.get_argument("charset")
        sign = self.get_argument("sign")
        sign_type = self.get_argument("sign_type")
        gmt_create = self.get_argument("gmt_create")
        gmt_payment = self.get_argument("gmt_payment", None)
        gmt_close = self.get_argument("gmt_close", None)

        # model = PPAliPayOrderModel()
        # model.notify_time = notify_time
        # model.notify_type = notify_type
        # model.notify_id = notify_id
        # model.subject = subject
        # model.body = body
        # model.app_id = app_id
        # model.seller_id = seller_id
        # model.seller_email = seller_email
        # model.buyer_id = buyer_id
        # model.auth_app_id = auth_app_id
        # model.buyer_logon_id = buyer_logon_id
        # model.fund_bill_list = fund_bill_list
        # model.fund_bill_list_account = fund_bill_list_account
        # model.fund_bill_list_fundChannel = fund_bill_list_fundChannel
        # model.trade_status = trade_status
        # model.total_amount = total_amount
        # model.invoice_amount = invoice_amount
        # model.receipt_amount = receipt_amount
        # model.buyer_pay_amount = buyer_pay_amount
        # model.point_amount = point_amount
        # model.version = version
        # model.out_trade_no = out_trade_no
        # model.trade_no = trade_no
        # model.charset = charset
        # model.sign = sign
        # model.sign_type = sign_type
        # model.gmt_create = gmt_create
        # model.gmt_payment = gmt_payment
        # model.gmt_close = gmt_close

        # # 更新到数据库
        # manager = PPAliPayOrderManager()
        # is_success = manager.update_order(model)
        # manager.closedb()

        # # 更新订单状态到打印任务数据表
        # manager = PPWXUnifyOrderManager()
        # _ = manager.update_printjob_status_by_out_trade_no("Paid", 2, out_trade_no)
        # manager.closedb()

        # # 查询商家的基本信息
        # manager = PPMerchantWithdrawalManager()
        # merchant_id, shop_name, university_name, city_name, wechat_realname, wechat_account, alipay_realname, alipay_account, transferedID = manager.query_merchant_payinfo_by_out_trade_no(out_trade_no)
        # manager.closedb()
        # if transferedID is not None and transferedID > 0:
        #     logger = PPLogger()
        #     logger.write("WeChat transferedID: "+str(transferedID))
        #     return

        # if alipay_realname is not None and alipay_account is not None:
        #     # 实时转账给商户
        #     # 转账额度 单日转出累计额度为 100 万元； 
        #     # 转账给个人支付宝账户，单笔最高 5 万元；
        #     # 转账给企业支付宝账户，单笔最高 10 万元。
        #     payee_account = alipay_account
        #     transfer_amount = float(fund_bill_list_account)
        #     payer_show_name = "印加加智能自助打印"
        #     payee_real_name = alipay_realname
        #     remark = shop_name + "-实时收款"
        #     alipay = PPAliPayAPI() 
        #     code, msg, order_id, out_biz_no, pay_date = alipay.transfer_to_alipay_account(out_trade_no, payee_account, transfer_amount, payer_show_name, payee_real_name, remark)
        #     # if int(code) == 10000:
        #     # 不管是成功，还是失败，都添加到数据库，以此来看是否转账成功
        #     # 添加到数据库
        #     transferredModel = PPTransferredRecordModel()
        #     transferredModel.merchant_id = merchant_id
        #     transferredModel.realname = alipay_realname 
        #     transferredModel.account = alipay_account
        #     transferredModel.amount = transfer_amount * 100 # 因为支付宝的单位是元，我们存储的值都是以INT型为主，而且是分的单位
        #     transferredModel.returned_code = code
        #     transferredModel.returned_msg = msg
        #     transferredModel.order_id = order_id
        #     transferredModel.out_biz_no = out_biz_no
        #     transferredModel.pay_date = pay_date
        #     transferredManager = PPTransferredRecordManager()
        #     transferredManager.add_alipay(transferredModel)
        #     transferredManager.closedb()
            # else:
            #     pass
                # 查询转账是否成功
                # out_biz_no = "54e7872de9c02793d5e76841ece20a3d"
                # order_id = "20190818110070001506610012088245"
                # alipay.query_transferred_to_alipay_account(out_biz_no, order_id)

        # 如果商户反馈给支付宝的字符不是success这7个字符，支付宝服务器会不断重发通知，直到超过24小时22分钟。
        # 一般情况下，25小时以内完成8次通知（通知的间隔频率一般是：4m,10m,10m,1h,2h,6h,15h）。 
        self.write("success")
        self.finish()

