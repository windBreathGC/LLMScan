from sanic import Sanic

from base.base import ServiceBase
from constants.constant import SANIC_NAME

app = Sanic.get_app(name=SANIC_NAME)


@app.main_process_start
async def main_process_start(sanic_app):
    # 创建数据库表结构
    print("main_process_start")


@app.after_server_start
async def after_server_start(sanic_app):
    await ServiceBase.get_service("prompt").init_prompts()
