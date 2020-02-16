import asyncio

from aiohttp import web
import socketio

from src.views import routes as user_routes

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
async def user_data(sid, data):
    print(data)


async def app_factory(*args):
    app = web.Application()
    sio.attach(app)
    app.add_routes(user_routes)
    return app


if __name__ == '__main__':
    sio.start_background_task(background_task)
    web.run_app(app_factory(), port=8000, reuse_address=True)
