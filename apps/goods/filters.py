from django_filters import rest_framework as django_filters
# import django_filters  # 这是错误的导入方式！
from goods.models import Goods

class GoodsFilter(django_filters.FilterSet):
    # 前端可以通过 http://127.0.0.1:8000/goods/?min_price=100&max_price=200&name=&is_hot= 来筛选商品
    min_price = django_filters.NumberFilter(field_name="shop_price", lookup_expr='gt')
    max_price = django_filters.NumberFilter(field_name="shop_price", lookup_expr='lt')
    name =django_filters.CharFilter(field_name = "name",lookup_expr = 'icontains') # contains 代表包含，i 代表不区分大小写
    class Meta:
        model = Goods
        # 前端可以请求 127.0.0.1:8000/goods/?is_hot=true 来获取热销商品
        fields = ['min_price', 'max_price','name', 'is_hot', 'is_new']
