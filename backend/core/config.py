# backend/core/config.py

from pydantic import AnyHttpUrl
from typing import List
from loguru import logger
import time
import os

class Settings:
    ENV = os.environ.get("fast_env", "DEV")  # 环境变量指定当前环境
    APP_NAME = "fastapi-vue-admin"
    # API 前缀
    API_PREFIX = "/api"
    # JWT 密钥
    SECRET_KEY = "ShsUP9qIP2Xui2GpXRY6y74v2JSVS0Q2YOXJ22VjwkI"
    # Token 过期时间
    ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60
    # 跨域白名单
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:9528"]
    # 数据库配置
    DB_URL = "mysql+pymysql://root:Aa123456@127.0.0.1:3306/fast"
    # 端口配置
    PORT = 8999
    # 是否启用热加载
    RELOAD = True

    # 定义上传文件、CMDB 模板和日志存储的文件夹路径
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件所在的目录
    UPLOAD_FOLDER = os.path.join(BASE_PATH, "..", "upload_files")  # 相对于项目根目录的路径
    CMDB_FOLDER = os.path.join(BASE_PATH, "..", "cmdb_files")
    LOG_FOLDER = os.path.join(BASE_PATH, "..", "fastapi_logs")

    # 创建文件夹如果它们不存在
    for folder in [UPLOAD_FOLDER, CMDB_FOLDER, LOG_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # 日志设置
    t = time.strftime("%Y_%m_%d")
    logger = logger
    logger.add(f"{LOG_FOLDER}/fastapi_log_{t}.log", rotation="00:00", encoding="utf-8", retention="30 days")

settings = Settings()
