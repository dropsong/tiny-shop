from django.http import HttpRequest
from users.models import UserProfile
from rest_framework import serializers
import re


# 官方推荐的写法在与 simplejwt 配合时会出现问题，所以这里自己写一个
def SelfQuerySet(request: HttpRequest, model_class):
    # 只能查看自己的内容
    cookie_header = request.headers.get('Cookie', '')
    match = re.search(r'name=([^;]+)', cookie_header)
    uname = ''
    if match:
        uname = match.group(1)
    uuser = UserProfile.objects.get(username=uname) # 若失败应当抛出异常
    return model_class.objects.filter(user=uuser)


def put_user(request, attrs):
    # put_user(self.context['request'], attrs)   # 用法
    cookie_header = request.headers.get('Cookie', '')
    match = re.search(r'name=([^;]+)', cookie_header)
    if match:
        name_value = match.group(1)
        try:
            user = UserProfile.objects.get(username=name_value)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("用户不存在")
        attrs['user'] = user
    else:
        raise serializers.ValidationError("Cookie 中未找到用户 name")
    return attrs
