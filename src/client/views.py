from aiohttp.web import View, json_response
from aiohttp_jinja2 import template
from bson import ObjectId


class CanvasView(View):
    @template('canvas.html')
    async def get(self):
        return


class GalleryView(View):
    def __init__(self, request):
        self.db = request.app['db']
        super().__init__(request)

    @template('gallery.html')
    async def get(self):
        record = await self.db.images.find_one({'_id': ObjectId(self.request.match_info['image_id'])})
        return {'image': record['image']}

    async def post(self):
        data = await self.request.post()
        record = await self.db.images.insert({'image': data['image']})
        return json_response({'id': str(record)})
