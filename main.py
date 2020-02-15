import asyncio

from aiohttp import web
import socketio

from src.views import routes as user_routes

sio = socketio.AsyncServer(async_mode='aiohttp')


async def background_task():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        await sio.sleep(10)
        count += 1
        await sio.emit('my_response', {'data': 'Server generated event'})


@sio.event
async def connect(sid, environ):
    await sio.emit('response', {'data': 'Connected'}, room=sid)


@sio.event
async def disconnect(sid):
    print(f'Disconnected {sid}')


async def app_factory(*args):
    new_app = web.Application()
    sio.attach(new_app)
    new_app.add_routes(user_routes)
    return new_app


if __name__ == '__main__':
    sio.start_background_task(background_task)
    web.run_app(app_factory(), port=8000, reuse_address=True)
