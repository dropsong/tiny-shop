from goods.filters import GoodsFilter
from goods.models import Banner, Goods, GoodsCategory
from goods.serializers import BannerSerializer, CategorySerializer, GoodsSerializer, IndexCategorySerializer
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins


class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "p"


# from rest_framework.authentication import TokenAuthentication

class GoodsListViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    商品列表页，分页，搜索，过滤，排序
    '''
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication,)  # 使用 Token 认证

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # filterset_fields = ['name', 'shop_price']
    filterset_class = GoodsFilter # 写完这句需要到 settings 中配置
    search_fields = ['name', 'goods_brief', 'goods_desc']
    ordering_fields = ['sold_num', 'shop_price']

    # http://127.0.0.1:8000/goods/?price_min=100
    def get_queryset(self) :
        queryset=Goods.objects.all() #这里只是拼接了 sql，并不会查询数据库所有数据
        price_min=self.request.query_params.get("price_min",0)
        if price_min:
            queryset=queryset.filter(shop_price__gt=int(price_min))
        return queryset


class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
    商品分类列表数据
    retrieve:
    获取商品分类详情
    """
    #和 Goods 很像，因为不需要分页，过滤，搜索等其他功能，所以通过下面两句即可
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    # is_tab 等于 True 就是顶部的快捷标签显示的那些
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"]) # 这里写死了，其实也可以配置
    serializer_class = IndexCategorySerializer
    # 一个模型类可以给多个 views 和 serializers 使用，但是需要保证 views 和 serializers 使用的是同一个，这样查询集才对得上。
