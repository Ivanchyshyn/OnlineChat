from aiohttp import web

routes = web.RouteTableDef()


@routes.view('/user/{name}')
class UserView(web.View):
    async def get(self):
        return web.json_response({'name': self.request.match_info['name']})
