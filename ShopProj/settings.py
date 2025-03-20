"""
Django settings for ShopProj project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

import sys, os
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# 这是一个无关紧要的练习项目，因此我选择不删除它
SECRET_KEY = 'django-insecure-tibk6!eepdmipfd5t=u2a$)%^ndo$4s6mbho_i005n#rnqeqz-'
# 这也是 JWT 的密钥

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# 用户相关使用这个模型类，createsuperuser 时使用自定义的用户模型
AUTH_USER_MODEL = 'users.UserProfile' 

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'goods',
    'trade',
    'user_operation',
    'users',
    'DjangoUeditor',
    'social_core',
    'crispy_forms',
    'reversion',
    'rest_framework',
    'rest_framework.authtoken',  # token 登录需要使用这个
    'django_filters',
    'corsheaders', # 支持跨域
    'drf_spectacular', # 自动生成 API 文档
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware', # 支持跨域
]

ROOT_URLCONF = 'ShopProj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  # 第三方登录
                'social_django.context_processors.login_redirect',  # 第三方登录
            ],
        },
    },
]

WSGI_APPLICATION = 'ShopProj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shop',             # 使用的数据库的名字,数据库必须手动创建
        'USER': 'root',             # 链接 mysql 的用户名
        'PASSWORD': 'zhiyue123',          # 用户对应的密码
        'HOST': 'localhost',        # 指定 mysql 数据库所在电脑 ip
        'PORT': 3306,               # mysql 服务的端口号
        'OPTIONS': {"init_command": "SET default_storage_engine=INNODB;"},
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = False  # 关闭时区自动检测


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK ={
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

CROS_ORIGIN_ALLOW_ALL = True  # 允许跨域

import datetime
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=17),
}

AUTHENTICATION_BACKENDS = (  # 只要满足一个即可
    'users.views.CustomBackend',
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.weibo.WeiboOAuth2',
)

# 手机号码正则表达式，这个正则并不会匹配所有手机号，而是作了限制
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
# 云片网（发送短信验证码）设置
APIKEY = "你知道的太多了"

# 支付宝相关配置
private_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/private_2048')
ali_pub_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/alipay_key_2048')

AZURE_SERVER_IP = "51.140.127.106"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 15
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SOCIAL_AUTH_WEIBO_KEY = '4130988826'
SOCIAL_AUTH_WEIBO_SECRET = '58982eecdbd586a3f1663f2bb89ea5dc'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/index/'
