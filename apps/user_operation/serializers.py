from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from ShopProj import settings
from goods.models import Goods
from users.models import UserProfile
from utils.diyfunc import put_user
from .models import UserFav
from .models import UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer
import re
import jwt


# CREATE  http://127.0.0.1:8000/userfavs/   payload:{goods: "1"}
class UserFavSerializer(serializers.ModelSerializer):

    # 不需要前端提交用户 id, 因为 JWT 中已经带了
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    def validate(self, attrs):
        return put_user(self.context['request'], attrs)

    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]
        fields = ("user", "goods", "id")
        

# DELETE  http://127.0.0.1:8000/userfavs/1/    # 风格不统一害死人，接口是谁写的？
class UserFavSerializer2(serializers.ModelSerializer):

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    def validate(self, attrs):

        request = self.context['request']
        cookie_header = request.headers.get('Cookie', '')
        token_match = re.search(r'token=([^;]+)', cookie_header)
        if token_match:
            token = token_match.group(1)
            try:
                # 解码 JWT 令牌
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('user_id')
                user = UserProfile.objects.get(id=user_id)
                attrs['user'] = user
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                raise serializers.ValidationError("无效的 token")
            except UserProfile.DoesNotExist:
                raise serializers.ValidationError("用户不存在")
        else:
            raise serializers.ValidationError("Cookie 中未找到 token")

        goods_id = self.context['view'].kwargs.get('goods_id') # ?
        try:
            goods = Goods.objects.get(id=goods_id)
            attrs['goods'] = goods
        except Goods.DoesNotExist:
            raise serializers.ValidationError("商品不存在")

        return attrs

    class Meta:
        model = UserFav  # 要在数据库中删除该对象的一个实例
        fields = ("user", "goods")
        # user_id = jwt 中解析出来的 user_id，通过这个 user_id 找到 UserProfile 对象赋给 user
        # goods_id 为链接后的参数，根据这个参数找到 Goods 对象赋给 goods


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()
    # 与 UserFavSerializer 差异在于我们的 goods 商品的详细信息
    class Meta:
        model = UserFav
        fields = ("goods", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # read_only 的作用就是只返回，不提交，也就是 post 时不需要用户提交
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    def validate(self, attrs):
        return put_user(self.context['request'], attrs)

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id" ,"add_time")


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    def validate(self, attrs):
        return put_user(self.context['request'], attrs)

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name",
                  "add_time", "signer_mobile")
