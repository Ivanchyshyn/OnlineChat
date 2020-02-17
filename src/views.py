import socketio

from src.models import Session, Message

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
    order_id = data['id']
    user_id = data['userId']
    # user_role = data['user_role']
    contractor_id = data.get('contractorId') or user_id
    room = f"{order_id}_{contractor_id}"
    sio.enter_room(sid, room)

    session = Session()
    filters = {
        'contractor_id': contractor_id,
        'order_id': order_id,
    }
    if user_id != contractor_id:
        filters['partner_id'] = user_id
    messages = session.query(Message).filter_by(**filters)
    messages = [message.to_json() for message in messages.all()]
    print('\nMessages', messages, '\n')
    session.close()
    await sio.emit(room, {'data': messages}, room=sid)


@sio.event
async def leave_room(sid, data):
    print('leave room')
    sio.leave_room(sid, data.get('id', 0))


@sio.event
async def create_message(sid, data):
    pass


@sio.event
async def hello(sid, data):
    print(data)
    await sio.emit('message{}'.format(data['room']), {'data': 'AAA'}, room=data['room'])
