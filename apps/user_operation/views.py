from django.db import IntegrityError
from rest_framework import viewsets, status, mixins

from user_operation.permissions import IsOwnerOrReadOnly
from users.models import UserProfile
from .models import UserAddress, UserFav, UserLeavingMessage
from .serializers import AddressSerializer, LeavingMessageSerializer, UserFavDetailSerializer, UserFavSerializer, UserFavSerializer2
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from utils.diyfunc import SelfQuerySet
import re


class UserFavViewset(mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin, # 详情页
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    用户收藏功能，CreateModelMixin 用来添加收藏，DestroyModelMixin 删除收藏
    '''

    permission_classes = (IsOwnerOrReadOnly,)
    # permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = "goods_id"     # 通过商品 id 来查找
    # 这种简单需求都需要深入源码去找，是否说明框架本身设计不够友好？

    def get_queryset(self):
        return SelfQuerySet(self.request, UserFav)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({"detail": "已经收藏"}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == "create":
            return UserFavSerializer
        elif self.action == "destroy":
            return UserFavSerializer2
        elif self.action == "list":
            return UserFavDetailSerializer


class LeavingMessageViewset(mixins.ListModelMixin, mixins.DestroyModelMixin,
                            mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    list:
    获取用户留言
    create:
    添加留言
    delete:
    删除留言功能
    """
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = LeavingMessageSerializer

    def get_queryset(self):
        return SelfQuerySet(self.request, UserLeavingMessage)


class AddressViewset(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = AddressSerializer

    def get_queryset(self):  
        return SelfQuerySet(self.request, UserAddress)
