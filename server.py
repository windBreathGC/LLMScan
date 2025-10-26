import platform
from pathlib import Path
from typing import Dict

import yaml
from sanic import Sanic
from sanic.log import LOGGING_CONFIG_DEFAULTS
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from yaml.parser import ParserError
from yaml.scanner import ScannerError

from base.base import ServiceBase
from constants.constant import SANIC_NAME


def get_config_content(file_path: Path) -> Dict:
    """解析yml文件"""
    if not file_path.exists() or not file_path.is_file():
        return {}
    with file_path.open(encoding="utf-8") as temp:
        try:
            return list(yaml.load_all(temp, Loader=yaml.SafeLoader))[0]
        except (yaml.scanner.ScannerError, yaml.parser.ParserError):
            return {}


# Sanic对于不同的操作系统，需要设置不同的启动方法，不然会报错
Sanic.START_METHOD_SET = True
Sanic.start_method = "spawn" if platform.system().lower() == "windows" else "fork"

content = get_config_content(Path("config", "config.yml"))
# 设置日志级别
log_level = content.get("log_level")
LOGGING_CONFIG_DEFAULTS["loggers"]["sanic.root"]["level"] = log_level
LOGGING_CONFIG_DEFAULTS["loggers"]["sanic.error"]["level"] = "ERROR"
# 创建数据库引擎，并采用异步的方式启动服务
engine = create_async_engine(content.get("database"), echo=True)
session = async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
ServiceBase.set_session(session())
# 启动服务，同时指定日志配置
app = Sanic(SANIC_NAME, log_config=LOGGING_CONFIG_DEFAULTS)

# 引入路由
import api.api

if __name__ == "__main__":
    app.run(host=content.get("host"), port=content.get("port"), debug=False, access_log=False)
