import platform

from sanic import Sanic
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from base.base import ServiceBase

# Sanic对于不同的操作系统，需要设置不同的启动方法，不然会报错
Sanic.START_METHOD_SET = True
Sanic.start_method = "spawm" if platform.system() == "windows" else "fork"

# 创建数据库引擎，并采用异步的方式启动服务
engine = create_async_engine("sqlite://", echo=True)
session = async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
ServiceBase.set_session(session())
