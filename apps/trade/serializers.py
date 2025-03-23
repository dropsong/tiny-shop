from rest_framework import serializers
from goods.serializers import GoodsSerializer
from goods.models import Goods
from utils.alipay_tools import AliPay
from utils.diyfunc import put_user
from .models import OrderGoods, OrderInfo, ShoppingCart
from ShopProj.settings import AZURE_SERVER_IP, ali_pub_key_path, private_key_path
import time


class ShopCartDetailSerializer(serializers.ModelSerializer) :
    '''
    列表页使用的序列化类
    '''
    goods = GoodsSerializer(many = False, read_only = True)
    class Meta :
        model = ShoppingCart
        fields = ("goods", "nums")


class ShopCartSerializer(serializers.Serializer) :

    user = serializers.HiddenField(
        default = serializers.CurrentUserDefault()
    )

    def validate(self, attrs):
        return put_user(self.context['request'], attrs)

    nums = serializers.IntegerField(required = True, label = "数量", min_value = 1,
                                    error_messages = {
                                        "min_value" : "商品数量不能小于一",
                                        "required" : "请选择购买数量"
                                    })

    goods = serializers.PrimaryKeyRelatedField(required = True, queryset = Goods.objects.all())

    def create(self, validated_data):
        nums = validated_data["nums"]
        goods = validated_data["goods"]
        existed = ShoppingCart.objects.filter(user = validated_data['user'], goods = goods)

        if existed :  # 购物车中已经有这个商品
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else :
            existed = ShoppingCart.objects.create(**validated_data)

        # 加入购物车几个就把商品库存减少几个
        goods = existed.goods
        goods.goods_num -= nums
        goods.save()
        return existed
    
    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


#用来显示订单详情中的商品详情
class OrderGoodsSerialzier(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)#一个商品id只会对应一件商品
    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerialzier(many=True)#一个订单id可以有多个商品
    #SerializerMethodField自定义的serializer，无需用户提交
    alipay_url = serializers.SerializerMethodField(read_only=True)
    # 这里的 alipay_url 和 get_alipay_url() 函数的名字是有严格对应关系的
    def get_alipay_url(self, obj):
        # alipay = AliPay(
        #     appid="2016101400687743",
        #     # app_notify_url="http://127.0.0.1/alipay/return/",
        #     app_notify_url="http://" + server_ip + "/alipay/return/",
        #     app_private_key_path=private_key_path,
        #     alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        #     debug=True,  # 默认False,
        #     return_url="http://" + server_ip + "/alipay/return/"
        # )

        # url = alipay.direct_pay(
        #     subject=obj.order_sn,
        #     out_trade_no=obj.order_sn,
        #     total_amount=obj.order_mount,
        # )
        # re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        # alipay 的沙箱环境有问题，这里跳过了
        re_url = "https://booking.com"
        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def generate_order_sn(self):
        # 当前时间 + userid + 随机数，生成订单号
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id, ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        '''
        前端不需要提交这个字段，后端自动生成
        '''
        put_user(self.context['request'], attrs)
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    # # SerializerMethodField 自定义的 serializer，无需用户提交
    # alipay_url = serializers.SerializerMethodField(read_only=True)

    # def get_alipay_url(self, obj):
    #     server_ip = AZURE_SERVER_IP
    #     alipay = AliPay(
    #         appid = "2016101400687743",
    #         # app_notify_url="http://127.0.0.1/alipay/return/",
    #         app_notify_url = "http://" + server_ip + "/alipay/return/",
    #         app_private_key_path = private_key_path,
    #         alipay_public_key_path = ali_pub_key_path, # 支付宝的公钥，验证支付宝回传消息使用
    #         debug = True, # 默认 False,
    #         return_url = "http://" + server_ip + "/alipay/return/"
    #     )

    #     url = alipay.direct_pay(
    #         subject=obj.order_sn,
    #         out_trade_no=obj.order_sn,
    #         total_amount=obj.order_mount,
    #     )
    #     re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

    #     return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"
