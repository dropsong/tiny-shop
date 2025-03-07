from rest_framework import serializers
from goods.serializers import GoodsSerializer
from goods.models import Goods
from users.models import UserProfile
from utils.diyfunc import put_user
from .models import OrderInfo, ShoppingCart
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

        return existed
    
    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


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

    class Meta:
        model = OrderInfo
        fields = "__all__"
