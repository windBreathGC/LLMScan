from sanic import Sanic
from sanic.response import json
from sqlalchemy import select, func

import api.listener
from base.base import ServiceBase
from constants.constant import SANIC_NAME
from model.model import PromptModel

app = Sanic.get_app(name=SANIC_NAME)


@app.route('/')
async def test(request):
    return json({'hello': 'world'})


@app.route('/prompt_count')
async def get_prompt_count(request):
    count = 0
    session = ServiceBase.get_service("prompt").session
    async with session:
        # 查询表总行数
        stmt = select(func.count()).select_from(PromptModel)
        result = await session.execute(stmt)
        count += result.scalar()
    return json(count)
