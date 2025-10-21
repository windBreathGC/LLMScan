from sanic import Sanic
from sanic.response import json

from constants.constant import SANIC_NAME

app = Sanic.get_app(name=SANIC_NAME, force_create=True)


@app.route('/')
async def test(request):
    return json({'hello': 'world'})
