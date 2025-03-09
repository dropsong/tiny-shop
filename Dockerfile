FROM python:3.11
WORKDIR /app
COPY . /app/

# 更新 apt 并安装 MySQL 客户端
RUN apt-get update && apt-get install -y default-mysql-client

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN chmod +x /app/start.sh

# 启动容器时执行数据库迁移、数据导入，并运行服务器
CMD ["/app/start.sh"]
