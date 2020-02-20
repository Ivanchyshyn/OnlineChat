import aioredis
from aiopg.sa import create_engine

from src import settings as bd_set
from src.views import app


async def redis_engine(cur_app):
    cur_app['redis'] = await aioredis.create_redis_pool(bd_set.REDIS_CACHE_URL)
    yield
    cur_app['redis'].close()
    await cur_app['redis'].wait_closed()


async def pg_engine(cur_app):
    cur_app['pg_engine'] = await create_engine(
        user=bd_set.PROD_PG_USER,
        database=bd_set.PROD_PG_NAME,
        host=bd_set.PROD_PG_HOST,
        password=bd_set.PROD_PG_PASSWORD,
        port=bd_set.PROD_PG_PORT,
    )
    yield
    cur_app['pg_engine'].close()
    await cur_app['pg_engine'].wait_closed()


app.cleanup_ctx.append(pg_engine)
app.cleanup_ctx.append(redis_engine)
# if __name__ == '__main__':
#     sio.start_background_task(background_task)
#     web.run_app(app, port=8000, reuse_address=True)
