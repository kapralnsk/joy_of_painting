from aiohttp.web import View, json_response, Response
from aiohttp_jinja2 import template, render_template

from base import BaseView


class CanvasView(View):
    @template('canvas.html')
    async def get(self):
        brushes = [
            {'name': 'Small brush', 'size': 2},
            {'name': 'Medium brush', 'size': 5},
            {'name': 'Big brush', 'size': 8},
        ]
        return {'brushes': brushes}


class ImageAPIView(BaseView):
    collection_name = 'images'
    required_params = {
        'get': ['image_id'],
        'post': ['image'],
        'put': ['image_id', 'image'],
        'delete': ['image_id']
    }

    async def get(self):
        record = await self.dao.retrieve(self.request.match_info['image_id'])
        return json_response({'image': record['image']})

    async def post(self):
        data = await self.request.post()
        record = await self.dao.create(dict(data))
        return json_response({'id': record})

    async def put(self):
        await self.request.post()
        data = self.request.POST
        await self.dao.update(
            self.request.match_info['image_id'],
            dict(data)
        )
        return json_response({'id': self.request.match_info['image_id']})

    async def delete(self):
        await self.dao.remove(self.request.match_info['image_id'])
        return Response()


class GalleryView(BaseView):
    collection_name = 'images'
    required_params = {
        'get': None
    }

    async def detail(self):
        return await self.dao.retrieve(self.request.match_info['image_id'])

    async def list(self):
        items = await self.dao.list()
        return {'items': items}

    async def get(self):
        if self.request.match_info.get('image_id'):
            context = await self.detail()
            template_name = 'gallery/detail.html'
        else:
            context = await self.list()
            template_name = 'gallery/list.html'
        return render_template(template_name, self.request, context)
