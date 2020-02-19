import json
from collections import namedtuple

User = namedtuple('User', 'full_name avatar')


async def get_user_information(user_id):
    from .views import app
    redis = app['redis']
    user_key = f'user_{user_id}'
    user = await redis.get(user_key, encoding='UTF-8')
    if user:
        user = json.loads(user)
        print('User from Redis', user)
        return User(user['full_name'], user['avatar'])

    async with app['pg_engine'].acquire() as con:
        result = await con.execute(
            'SELECT first_name, last_name, avatar FROM users_customuser WHERE id=%s', (user_id,)
        )
        result = await result.first()
        print('Result', result)
        if result:
            first_name, last_name, avatar = result.as_tuple()
            full_name = '{} {}'.format(first_name or '', last_name or '').strip()
            print('Set user to Redis', full_name, avatar)
            user_data = json.dumps({'full_name': full_name, 'avatar': avatar})
            await redis.set(user_key, user_data, expire=60 * 60 * 24)
            return User(full_name, avatar)
        return User('', None)
