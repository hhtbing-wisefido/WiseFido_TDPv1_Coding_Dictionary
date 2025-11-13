# Dockerfile for WiseFido Medical Coding Dictionary API
# 基于 Python 3.13 Alpine 构建轻量级镜像

FROM python:3.13-alpine

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY app.py .
COPY scripts/ ./scripts/
COPY coding_dictionary/ ./coding_dictionary/
COPY schema/ ./schema/

# 创建非 root 用户
RUN adduser -D -u 1000 appuser && \
    chown -R appuser:appuser /app

# 切换到非 root 用户
USER appuser

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:8080/api/health || exit 1

# 启动命令
CMD ["python", "app.py"]
