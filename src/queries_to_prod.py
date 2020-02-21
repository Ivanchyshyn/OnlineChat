import json

from .utils import NamedUser


class DatabaseQuery:
    """Class that works with databases connections"""

    def __init__(self, app):
        """
        :param app: Current running web app
        :type app: aiohttp.web.Application
        """
        self.app = app

    async def get_user_information(self, user_id) -> NamedUser:
        redis = self.app['redis']
        user = await redis.get(f'user_{user_id}', encoding='UTF-8')
        if user:
            user = json.loads(user)
            print('User from Redis', user)
            return NamedUser(user['full_name'], user['avatar'])

        return await self.get_user_from_prod(user_id)

    async def get_user_from_prod(self, user_id):
        async with self.app['pg_engine'].acquire() as con:
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
                await self.app['redis'].set(f'user_{user_id}', user_data, expire=60 * 60 * 24)
                return NamedUser(full_name, avatar)
            return NamedUser('', None)
