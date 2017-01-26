import inspect
from aiohttp.web import View, json_response
from bson import ObjectId


def request_handler_wrapper(func):
    async def wrapped(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            return json_response({'error_message': str(e)}, status=500)
    return wrapped


class BaseView(View):
    collection_name = None

    def __init__(self, request, dao=None):
        super().__init__(request)
        db = self.request.app['db']
        if dao:
            self.dao = dao
        elif not dao and self.collection_name:
            self.dao = BaseDAO(db[self.collection_name])

        # wrap methods in request_handler_wrapper
        for name, m in inspect.getmembers(self, inspect.ismethod):
            if name in ['get', 'post', 'put', 'delete']:
                setattr(self, name, request_handler_wrapper(m))


class BaseDAO(object):
    def __init__(self, collection):
        self.collection = collection

    async def create(self, **kwargs):
        record = await self.collection.insert(kwargs)
        return str(record)

    async def update(self, object_id, **kwargs):
        record = await self.collection(
            {'_id': ObjectId(object_id)},
            kwargs
        )
        return str(record)

    async def remove(self, object_id):
        await self.collection.delete_one({'_id': ObjectId(object_id)})
        return True

    async def retrieve(self, object_id):
        record = await self.collection.find_one({'_id': ObjectId(object_id)})
        return self._replace_object_id(record)

    async def list(self):
        items = await self.collection.find()
        return list(map(lambda record: self._replace_object_id(record), items))

    @staticmethod
    def _replace_object_id(record):
        record['id'] = str(record.pop('_id'))
        return record
