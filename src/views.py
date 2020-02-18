import socketio

from src.database_utils import query_database
from src.models import Message
from src.utils import parse_data, get_filters

sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')


async def background_task():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        await sio.sleep(10)
        print('Sending task')
        count += 1
        await sio.emit('news', {'data': f'Server generated event {count}'})


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
    messages = [message.to_json() for message in messages]
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
    await sio.emit('incoming_' + result.room, {'data': message.to_json()}, room=result.room)


@sio.event
async def hello(sid, data):
    print(data)
    await sio.emit('message{}'.format(data['room']), {'data': 'AAA'}, room=data['room'])
