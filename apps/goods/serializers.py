from rest_framework import serializers
from goods.models import Banner, Goods, GoodsCategory, GoodsCategoryBrand, GoodsImage, IndexAd
from django.db.models import Q


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


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


# 首页商品分类显示功能，商品的品牌信息
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


# 商品分类显示序列化类
class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)  # 首先是拿到品牌信息，品牌表中的 Category id 是外键
    goods = serializers.SerializerMethodField()  # Category 是最顶级的，下面没有商品，所以不能用 GoodsSerializer，这个是最右边的商品
    sub_cat = CategorySerializer2(many=True)  # 左下角的二级分类数据
    ad_goods = serializers.SerializerMethodField()  # 处于从中间大图的广告位

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id, ) # model = GoodsCategory
        if ad_goods:  # 如果广告表中有数据
            good_ins = ad_goods[0].goods
            # 加入context={'request': self.context['request']}的作用是，图片资源带有访问的url，在view中我们调用serializer时，看ListModelMixin上下文是自动传进来的，而我们自己的serializer在调用serializer时，是没有的，所以我们自己加上
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return goods_json

    # 对应上面 goods 字段
    def get_goods(self, obj):
        # 找到某个大类下的所有商品
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))

        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data  # goods_serializer.data里边存的json数据

    class Meta:
        model = GoodsCategory
        fields = "__all__"
