import aiopg.sa as pg
import aioredis

from .settings import REDIS_CACHE_URL, PROD_PG_USER, PROD_PG_HOST, PROD_PG_NAME, PROD_PG_PASSWORD, PROD_PG_PORT


async def redis_engine(cur_app):
    cur_app['redis'] = await aioredis.create_redis_pool(REDIS_CACHE_URL)
    yield
    cur_app['redis'].close()
    await cur_app['redis'].wait_closed()


async def pg_engine(cur_app):
    cur_app['pg_engine'] = await pg.create_engine(
        user=PROD_PG_USER,
        database=PROD_PG_NAME,
        host=PROD_PG_HOST,
        password=PROD_PG_PASSWORD,
        port=PROD_PG_PORT,
    )
    yield
    cur_app['pg_engine'].close()
    await cur_app['pg_engine'].wait_closed()
