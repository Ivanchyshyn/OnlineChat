import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from src.models import Session


async def query_database(model, data, method='select'):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=1) as pool:
        result = await loop.run_in_executor(
            pool, partial(QUERY_TYPE[method], model, data))
    return result


def _query(model, filters):
    session = Session()
    result = session.query(model).filter_by(**filters).all()
    session.close()
    return result


def _insert(model, data):
    session = Session(expire_on_commit=False)
    message = model(**data)
    session.add(message)
    session.commit()
    session.close()
    return message


QUERY_TYPE = {
    'select': _query,
    'insert': _insert,
}
