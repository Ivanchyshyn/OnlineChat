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


def paginate(query, page, page_size):
    if page <= 0:
        raise AttributeError('page needs to be >= 1')
    if page_size <= 0:
        raise AttributeError('page_size needs to be >= 1')
    items = query.limit(page_size).offset((page - 1) * page_size).all()
    return items


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


def _select(model, data):
    page = data.pop('page', None)
    page_size = data.pop('page_size', 10)
    with session_scope(expire_on_commit=False) as session:
        query = session.query(model).filter_by(**data)
        total = query.order_by(None).count()
        if page:
            print('PAGINATING', page, page_size)
            result = reversed(
                paginate(query.order_by(model.created.desc()), page, page_size)
            )
        else:
            print('NOT PAGINATING')
            result = query.order_by(model.created).all()
        return result, total


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
    'select': _select,
    'insert': _insert,
    'update': _update,
    'delete': _delete,
}
