from sanic import Sanic
from sanic.response import json

from constants.constant import SANIC_NAME

app = Sanic(SANIC_NAME)


@app.route('/')
async def test(request):
    return json({'hello': 'world'})
