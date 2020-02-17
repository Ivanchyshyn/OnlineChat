import asyncio

from aiohttp import web

from src.views import sio


async def app_factory(*args):
    app = web.Application()
    sio.attach(app)
    return app


if __name__ == '__main__':
    # sio.start_background_task(background_task)
    web.run_app(app_factory(), port=8000, reuse_address=True)
