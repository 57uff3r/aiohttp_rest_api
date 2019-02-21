import os
from aiohttp import web
from aiohttp_rest.loader import load_and_connect_all_endpoints_from_folder

async def hello(request):
    return web.Response(text="Hello, world")

app = web.Application()
load_and_connect_all_endpoints_from_folder('{0}/{1}'.format(os.path.dirname(os.path.realpath(__file__)), 'endpoints'), app=app)
web.run_app(app)