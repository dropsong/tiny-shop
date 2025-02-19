# -*- coding: utf-8 -*-

# 独立使用django的model
import sys
import os


pwd = os.path.dirname(os.path.realpath(__file__))
print(pwd)
# sys.path.append(pwd+"../")
sys.path.append(os.path.join(pwd, "../"))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ShopProj.settings') # 将 setting 放入环境变量中，这一句和wsgi.py中的是一样的


import django
django.setup()  # 之后才可以做在 view 里面做的事情

from goods.models import GoodsCategory  #注意这一句不能够放到上面去

from db_tools.data.category_data import row_data

# allGategory= GoodsCategory.objects.all()#首先我们可以点击右键运行测试一下上面from是否OK
for lev1_cat in row_data:
    lev1_intance = GoodsCategory() # 初始一个对象并赋值，赋值后save
    lev1_intance.code = lev1_cat["code"]
    lev1_intance.name = lev1_cat["name"]
    lev1_intance.category_type = 1
    lev1_intance.save()

    for lev2_cat in lev1_cat["sub_categorys"]:
        lev2_intance = GoodsCategory()
        lev2_intance.code = lev2_cat["code"]
        lev2_intance.name = lev2_cat["name"]
        lev2_intance.category_type = 2
        lev2_intance.parent_category = lev1_intance
        lev2_intance.save()

        for lev3_cat in lev2_cat["sub_categorys"]:
            lev3_intance = GoodsCategory()
            lev3_intance.code = lev3_cat["code"]
            lev3_intance.name = lev3_cat["name"]
            lev3_intance.category_type = 3
            lev3_intance.parent_category = lev2_intance
            lev3_intance.save()

