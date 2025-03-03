from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from random import choice
from ShopProj.settings import APIKEY
from utils.yunpian import YunPian
from .models import VerifyCode

User = get_user_model()   # 获取用户模型


class CustomBackend(ModelBackend):  # 继承 ModelBackend 类
    """
    自定义用户验证
    """
    # 重写 authenticate 方法，仿照原来的函数写就行，注意返回类型
    def authenticate(self, request,username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


from .serializers import SmsSerializer, UserRegSerializer
from rest_framework_simplejwt.tokens import SlidingToken
from rest_framework.response import Response
from rest_framework import status

class UserViewset(CreateModelMixin,viewsets.GenericViewSet):
    """
    用户，GET 方法不允许
    """
    serializer_class = UserRegSerializer

    def perform_create(self, serializer):
        return serializer.save()  # 其实这里就是比原来的方法多一个 return

    def create(self, request, *args, **kwargs):
        # 问题：注册之后，浏览器 F12 看不到 token 和 name
        # 分析：实际上注册之后并没有登录，若想要登录，需要仿照登录的返回数据格式
        # 新增后的返回格式是由序列化类中的 fileds 决定的，若需改变，应重写 create 方法
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        # 拿到 serializer.data 然后将 name 和 token 填写进去
        re_dict = serializer.data
        re_dict["token"] = str(SlidingToken.for_user(user))
        re_dict["name"] = user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    #设置序列化类
    serializer_class = SmsSerializer

    #产生随机数
    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    # 重写 CreateModelMixin 的 create 方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]
        yun_pian = YunPian(APIKEY)

        # 生产随机验证码并发送
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        # 云片网的响应，返回 0 代表成功
        if sms_status["code"] != 0:
            return Response({
                "mobile":sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)

        else:
            # 保存验证码至后端
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile":mobile
            }, status=status.HTTP_201_CREATED)
