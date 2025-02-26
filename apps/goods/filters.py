# from django_filters import rest_framework as django_filters
import django_filters
from goods.models import Goods

# 这块实际上不起作用，就不用了
class GoodsFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="shop_price", lookup_expr='gt')
    max_price = django_filters.NumberFilter(field_name="shop_price", lookup_expr='lt')
    name =django_filters.CharFilter(field_name = "name",lookup_expr = 'icontains') # contains 代表包含，i 代表不区分大小写
    class Meta:
        model = Goods
        fields = ['min_price', 'max_price','name']
