import asyncio
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from functools import partial

from src.models import Session


async def query_database(model, data, method='select'):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=1) as pool:
        result = await loop.run_in_executor(
            pool, partial(QUERY_TYPE[method], model, data))
    return result


@contextmanager
def session_scope(**kwargs):
    session = Session(**kwargs)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def _query(model, filters):
    with session_scope(expire_on_commit=False) as session:
        result = session.query(model).filter_by(**filters).order_by(model.created).all()
        return result


def _insert(model, data):
    with session_scope(expire_on_commit=False) as session:
        obj = model(**data)
        session.add(obj)
        return obj


def _update(model, data):
    with session_scope() as session:
        print('Update DATA', data)
        message_id = data['message_id']
        row_count = session.query(model).filter_by(message_id=message_id).update({model.text: data['text']})
        print('ROW COUNT', row_count)
        session.commit()

        obj = session.query(model).get(message_id)
        print('MESSAGE', obj)
        session.close()
        return obj


def _delete(model, data):
    print('Remove Data', data)
    message_id = data['message_id']
    with session_scope() as session:
        obj = session.query(model).get(message_id)
        session.delete(obj)
    return message_id


QUERY_TYPE = {
    'select': _query,
    'insert': _insert,
    'update': _update,
    'delete': _delete,
}
