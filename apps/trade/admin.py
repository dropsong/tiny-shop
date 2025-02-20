from django.contrib import admin
from .models import ShoppingCart, OrderInfo, OrderGoods

class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ["user", "goods", "nums", ]


class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ["user", "order_sn",  "trade_no", "pay_status", "post_script", "order_mount",
                    "order_mount", "pay_time", "add_time"]

    # 内联模型管理类，用于在 OrderInfoAdmin 中嵌入 OrderGoods 模型。它允许在编辑 OrderInfo 实例时，同时管理相关的 OrderGoods 实例。
    class OrderGoodsInline(admin.TabularInline):
        model = OrderGoods
        exclude = ['add_time', ]
        extra = 1
        style = 'tab'

    inlines = [OrderGoodsInline, ]


admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)
