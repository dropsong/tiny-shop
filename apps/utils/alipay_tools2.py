import logging
import traceback

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.FileItem import FileItem
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradePayModel import AlipayTradePayModel
from alipay.aop.api.domain.GoodsDetail import GoodsDetail
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
from alipay.aop.api.domain.SettleInfo import SettleInfo
from alipay.aop.api.domain.SubMerchant import SubMerchant
from alipay.aop.api.request.AlipayOfflineMaterialImageUploadRequest import AlipayOfflineMaterialImageUploadRequest
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradePayRequest import AlipayTradePayRequest
from alipay.aop.api.response.AlipayOfflineMaterialImageUploadResponse import AlipayOfflineMaterialImageUploadResponse
from alipay.aop.api.response.AlipayTradePayResponse import AlipayTradePayResponse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')

def fix_base64_padding(data):
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    return data

if __name__ == '__main__':
    """
    设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
    """
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '9021000146606779'
    
    with open('../trade/keys/private_2048.txt', 'r') as f:
        private_key = f.read()
    private_key = fix_base64_padding(private_key)
    alipay_client_config.app_private_key = private_key
    
    with open('../trade/keys/alipay_key_2048.txt', 'r') as f:
        alipay_client_config.alipay_public_key = f.read()

    """
    得到客户端对象。
    注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
    logger参数用于打印日志，不传则不打印，建议传递。
    """
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)

    """
    页面接口示例：alipay.trade.page.pay
    """
    # 对照接口文档，构造请求对象
    model = AlipayTradePagePayModel()
    model.out_trade_no = "pay201805020000226"
    model.total_amount = 50
    model.subject = "测试"
    model.body = "支付宝测试"
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    settle_detail_info = SettleDetailInfo()
    settle_detail_info.amount = 50
    settle_detail_info.trans_in_type = "userId"
    settle_detail_info.trans_in = "2088302300165604"
    settle_detail_infos = list()
    settle_detail_infos.append(settle_detail_info)
    settle_info = SettleInfo()
    settle_info.settle_detail_infos = settle_detail_infos
    model.settle_info = settle_info
    sub_merchant = SubMerchant()
    sub_merchant.merchant_id = "2088301300153242"
    model.sub_merchant = sub_merchant
    request = AlipayTradePagePayRequest(biz_model=model)
    # 得到构造的请求，如果 http_method 是 GET，则是一个带完成请求参数的 url，如果 http_method 是 POST，则是一段 HTML 表单片段
    response = client.page_execute(request, http_method="GET")
    print("alipay.trade.page.pay response:" + response)
