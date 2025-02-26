from goods.models import Goods, GoodsCategory
from goods.serializers import CategorySerializer, GoodsSerializer
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins


class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "p"


class GoodsListViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    商品列表页，分页，搜索，过滤，排序
    '''
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'shop_price']
    search_fields = ['name', 'goods_brief', 'goods_desc']
    ordering_fields = ['sold_num', 'shop_price']

    # filter_class = GoodsFilter # 写完这句需要到 settings 中配置 # 无用

    # def get_queryset(self):
    #     return Goods.objects.filter(shop_price__gt=100)

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