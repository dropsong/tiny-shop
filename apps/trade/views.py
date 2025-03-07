from rest_framework import viewsets, mixins
from trade.models import OrderGoods, OrderInfo, ShoppingCart
from trade.serializers import OrderSerializer, ShopCartDetailSerializer, ShopCartSerializer
from user_operation.permissions import IsOwnerOrReadOnly
from utils.diyfunc import SelfQuerySet

class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    购物车功能
    list:
    获取购物车详情
    create：
    加入购物车
    delete：
    删除购物记录
    """
    lookup_field = 'goods_id' # 为修改、删除提供的依据，默认是主键，现在改变了
    # TODO   delete 方法需要权限控制

    # get queryset 只是限制了查询的范围，不会限制删除，因此需要限制删除权限
    def get_queryset(self):  
        return SelfQuerySet(self.request, ShoppingCart)

    def get_serializer_class(self):
        if self.action == "list":
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer


class OrderViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet) :
    """
    订单管理
    list:
    获取个人订单
    delete:
    删除订单
    create：
    新增订单
    """
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return SelfQuerySet(self.request, OrderInfo)

    # perform_create 用于对实例进行修改
    def perform_create(self, serializer):
        order = serializer.save()
        # 拿到购物车中的信息
        shop_carts = SelfQuerySet(self.request, ShoppingCart)

        order_mount = 0
        # 遍历购物车
        for shop_cart in shop_carts :
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_mount += shop_cart.goods.shop_price * shop_cart.nums
            order_goods.order = order
            # 订单商品信息保存
            order_goods.save()
            # 清空购物车
            shop_cart.delete()

        order.order_mount = order_mount
        order.save()
        return order
