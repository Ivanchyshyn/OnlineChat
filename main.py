import aioredis
from aiohttp import web
from aiopg.sa import create_engine

from src import settings as pg_set
from src.views import app


async def redis_engine(cur_app):
    cur_app['redis'] = await aioredis.create_redis_pool('redis://localhost/')
    yield
    cur_app['redis'].close()
    await cur_app['redis'].wait_closed()


async def pg_engine(cur_app):
    cur_app['pg_engine'] = await create_engine(
        user=pg_set.PROD_PG_USER,
        database=pg_set.PROD_PG_NAME,
        host=pg_set.PROD_PG_HOST,
        password=pg_set.PROD_PG_PASSWORD,
        port=pg_set.PROD_PG_PORT,
    )
    yield
    cur_app['pg_engine'].close()
    await cur_app['pg_engine'].wait_closed()


if __name__ == '__main__':
    # sio.start_background_task(background_task)
    app.cleanup_ctx.append(pg_engine)
    app.cleanup_ctx.append(redis_engine)
    web.run_app(app, port=8000, reuse_address=True)
