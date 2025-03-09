#!/bin/sh

python3 manage.py migrate
python3 /app/ShopProj/db_tools/import_goods_data.py
python3 /app/ShopProj/db_tools/import_category_data.py
python3 manage.py runserver 0.0.0.0:8000
