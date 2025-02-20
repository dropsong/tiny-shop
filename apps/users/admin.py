from django.contrib import admin
from .models import VerifyCode


class BaseSetting(admin.ModelAdmin):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(admin.ModelAdmin):
    site_title = "我的生鲜后台"
    site_footer = "ShopProj"
    # menu_style = "accordion"


class VerifyCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'mobile', "add_time"]


admin.site.register(VerifyCode, VerifyCodeAdmin)
# admin.site.register(BaseAdminView, BaseSetting)
# admin.site.register(CommAdminView, GlobalSettings)