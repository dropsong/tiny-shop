from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

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
