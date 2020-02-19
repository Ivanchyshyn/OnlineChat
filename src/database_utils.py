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
    result = session.query(model).filter_by(**filters).order_by(model.created).all()
    session.close()
    return result


def _insert(model, data):
    session = Session(expire_on_commit=False)
    message = model(**data)
    session.add(message)
    session.commit()
    session.close()
    return message


def _update(model, data):
    session = Session()
    print('Update DATA', data)
    message_id = data['message_id']
    row_count = session.query(model).filter_by(message_id=message_id).update({model.text: data['text']})
    print('ROW COUNT', row_count)
    session.commit()
    if not row_count:
        return

    message = session.query(model).get(message_id)
    print('MESSAGE', message)
    session.close()
    return message


def _delete(model, data):
    session = Session()
    print('Remove Data', data)
    message_id = data['message_id']
    obj = session.query(model).get(message_id)
    session.delete(obj)
    session.commit()
    session.close()
    return message_id


QUERY_TYPE = {
    'select': _query,
    'insert': _insert,
    'update': _update,
    'delete': _delete,
}
