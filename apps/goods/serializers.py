from rest_framework import serializers
from goods.models import Goods, GoodsCategory

class GoodsSerializer(serializers.ModelSerializer):
    class Meta :
        model = Goods
        # fields = [ 'name', 'click_num', 'market_price', 'goods_brief', 'goods_desc' ]
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)  # sub_cat 是 models 中的 related_name
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"
