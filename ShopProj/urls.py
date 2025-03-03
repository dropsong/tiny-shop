"""
URL configuration for ShopProj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path

from ShopProj.settings import MEDIA_ROOT
from django.views.static import serve
from goods.views import CategoryViewset, GoodsListViewSet
from rest_framework.routers import DefaultRouter

# from rest_framework.authtoken import views # 用于理解 token
from rest_framework_simplejwt.views import TokenObtainSlidingView
from users.views import UserViewset

router = DefaultRouter()
router.register(r'goods', GoodsListViewSet)
router.register(r'categorys', CategoryViewset)
router.register(r'users', UserViewset, basename="users") # 注册验证

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('api-auth/', include('rest_framework.urls')),  # 这个好像是 xadmin 用的，之后考虑删除
    # 支持静态资源文件的加载
    # 例如用户上传的资源，我们只要解决上传的功能就行，将资源放到对应目录下

    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # re_path(r'^api-token-auth/', views.obtain_auth_token), # 用于理解 token

    # path('jwt-auth/', TokenObtainPairView.as_view()), # 理解 jwt
    # path('jwt-refresh/', TokenRefreshView.as_view()), # 这两行仅演示，实际项目不会用到

    path('login/', TokenObtainSlidingView.as_view()),

    path('', include(router.urls)),
]
