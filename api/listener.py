from sanic import Sanic

from constants.constant import SANIC_NAME

app = Sanic.get_app(name=SANIC_NAME)


@app.main_process_start
async def main_process_start(sanic_app):
    # 创建数据库表结构
    print("main_process_start")
