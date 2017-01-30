from aiohttp.web import View, HTTPBadRequest
from bson import ObjectId


class BaseView(View):
    collection_name = None
    required_params = None

    def __init__(self, request, dao=None):
        super().__init__(request)
        db = self.request.app['db']
        if dao:
            self.dao = dao
        elif not dao and self.collection_name:
            self.dao = BaseDAO(db[self.collection_name])

        # add request validator to handler
        self.method_name = self.request.method.lower()
        request_handler = getattr(self, self.method_name)
        setattr(self, self.method_name, self.request_validator(request_handler))


    def request_validator(self, func):
        async def wrapped(*args, **kwargs):
            if self.method_name != 'get':
                await self.request.post()
                data = self.request.POST
            else:
                data = self.request.GET
            params = self.required_params[self.method_name]
            if params:
                for param in params:
                    if not data.get(param) and not self.request.match_info.get(param):
                        raise HTTPBadRequest(text=f'Missing required parameter {param}')
            return await func(*args, **kwargs)

        return wrapped


class BaseDAO(object):
    def __init__(self, collection):
        self.collection = collection

    async def create(self, data):
        record = await self.collection.insert(data)
        return str(record)

    async def update(self, object_id, data):
        record = await self.collection.update(
            {'_id': ObjectId(object_id)},
            data
        )
        return str(record)

    async def remove(self, object_id):
        await self.collection.delete_one({'_id': ObjectId(object_id)})
        return True

    async def retrieve(self, object_id):
        record = await self.collection.find_one({'_id': ObjectId(object_id)})
        return self._replace_object_id(record)

    async def list(self):
        items = await self.collection.find().to_list(length=None)
        return list(map(lambda record: self._replace_object_id(record), items))

    @staticmethod
    def _replace_object_id(record):
        record['id'] = str(record.pop('_id'))
        return record
