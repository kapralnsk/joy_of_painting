import asyncio

import aiohttp_jinja2
import jinja2
from aiohttp import web

from db import db
from client import routes

loop = asyncio.get_event_loop()
app = web.Application(loop=loop)
app['db'] = db

app.router.add_static('/static', 'src/static/')
for route in routes:
    app.router.add_route('*', route[0], route[1])

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('src/templates'))
web.run_app(app, host='0.0.0.0', port=8080)
