from rest_framework import serializers
from goods.models import Goods, GoodsCategory, GoodsImage


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image", )


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


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)  # 关联该字段
    class Meta :
        model = Goods
        # fields = [ 'name', 'click_num', 'market_price', 'goods_brief', 'goods_desc' ]
        fields = '__all__'
