# 使用官方轻量级 Python 3.9 镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装依赖
# 新增了 jinja2 用于渲染网页
RUN pip install --no-cache-dir \
    sanic \
    sanic-ext \
    httpx \
    requests \
    tqdm \
    aiosqlite \
    jinja2

# 创建数据目录
RUN mkdir -p /app/data

# 复制 Python 代码
COPY app.py .
# 复制 HTML 模板文件夹
COPY templates/ ./templates/

# 暴露端口
EXPOSE 8000

CMD ["python", "app.py"]
