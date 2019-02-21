import os
from aiohttp import web
from aiohttp_rest.loader import load_and_connect_all_endpoints_from_folder

import logging
logging.basicConfig(level=logging.DEBUG)
# logger = logging.Logger('aiohttp_rest')
# logger.setLevel(logging.DEBUG)

async def hello(request):
    return web.Response(text="Hello, world")

app = web.Application()
load_and_connect_all_endpoints_from_folder(
    path='{0}/{1}'.format(os.path.dirname(os.path.realpath(__file__)), 'endpoints'),
    app=app,
    version_prefix='v1'
)

web.run_app(app)