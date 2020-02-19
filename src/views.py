import socketio
from aiohttp import web

from src.database_utils import query_database
from src.models import Message
from src.utils import parse_data, get_filters, validate_fields


def app_factory(*args):
    _app = web.Application()
    sio.attach(_app)
    return _app


sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = app_factory()


@sio.event
async def connect(sid, environ):
    print('CONNECT')
    await sio.emit('response', {'data': 'Connected'}, room=sid)


@sio.event
async def disconnect(sid):
    print(f'Disconnected {sid}')


@sio.event
async def join_room(sid, data):
    print('join room', data)
    result = parse_data(data)
    sio.enter_room(sid, result.room)

    filters = get_filters(result)
    messages = await query_database(Message, filters)
    messages = [await message.to_json() for message in messages]
    print('\nMessages', messages, '\n')

    await sio.emit(result.room, {'data': messages}, room=sid)


@sio.event
async def leave_room(sid, data):
    sio.leave_room(sid, data['room'])


@sio.event
async def leave_all_rooms(sid, *data):
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
    print('\nNEW Message', message, sep='\n')
    await sio.emit('incoming_' + result.room, {'data': await message.to_json()}, room=result.room)


@sio.event
async def edit_message(sid, data):
    room = data.pop('room', None)
    if not room or not validate_fields(data, ['message_id', 'text']):
        return
    message = await query_database(Message, data, method='update')
    if message:
        await sio.emit('edited_' + room, {'data': await message.to_json()}, room=room)


@sio.event
async def delete_message(sid, data):
    room = data.pop('room', None)
    if not room or not validate_fields(data, ['message_id']):
        return
    message_id = await query_database(Message, data, method='delete')
    if message_id:
        await sio.emit('deleted_' + room, {'message_id': message_id}, room=room)
