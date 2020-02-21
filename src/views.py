import socketio
from aiohttp import web

from .app_engines import pg_engine, redis_engine
from .database_utils import query_database
from .models import Message
from .queries_to_prod import DatabaseQuery
from .utils import parse_data, get_filters, validate_fields

sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')


async def app_factory(*args):
    app = web.Application()
    sio.attach(app)
    sio.__myapp = app
    app.cleanup_ctx.append(pg_engine)
    app.cleanup_ctx.append(redis_engine)
    return app


@sio.event
async def connect(sid, environ):
    print('CONNECT')
    await sio.emit('response', {'data': 'Connected'}, room=sid)


@sio.event
async def disconnect(sid):
    print(f'Disconnected {sid}')


@sio.event
async def join_room(sid, data):
    print('\njoin room', data)
    result = parse_data(data)
    sio.enter_room(sid, result.room)

    filters = get_filters(result)
    filters.update({'page': result.page, 'page_size': result.page_size})
    messages, total = await query_database(Message, filters)
    database = DatabaseQuery(sio.__myapp)
    messages = [await message.to_json(database) for message in messages]
    print(f'\nTotal - {total}\nMessages - {messages}\n')

    await sio.emit(result.room, {'data': messages, 'total': total}, room=sid)


@sio.event
async def leave_room(sid, data):
    sio.leave_room(sid, data['room'])


@sio.event
async def leave_all_rooms(sid, *data, ):
    print('LEAVE ALL ROOMS', sio.rooms(sid), sid)
    for room in sio.rooms(sid):
        if room != sid:
            sio.leave_room(sid, room)


@sio.event
async def create_message(sid, data):
    result = parse_data(data)
    message_data = {
        'partner_id': result.partner,
        'order_id': result.order,
        'contractor_id': result.contractor,
        'sender_id': result.user,
        'text': data['text'],
    }
    message = await query_database(Message, message_data, method='insert')
    database = DatabaseQuery(sio.__myapp)
    print('\nNEW Message', message, sep='\n')
    await sio.emit('incoming_' + result.room, {'data': await message.to_json(database)}, room=result.room)


@sio.event
async def edit_message(sid, data):
    room = data.pop('room', None)
    if not room or not validate_fields(data, ['message_id', 'text']):
        return
    message = await query_database(Message, data, method='update')
    if message:
        database = DatabaseQuery(sio.__myapp)
        await sio.emit('edited_' + room, {'data': await message.to_json(database)}, room=room)


@sio.event
async def delete_message(sid, data):
    room = data.pop('room', None)
    if not room or not validate_fields(data, ['message_id']):
        return
    message_id = await query_database(Message, data, method='delete')
    if message_id:
        await sio.emit('deleted_' + room, {'message_id': message_id}, room=room)
