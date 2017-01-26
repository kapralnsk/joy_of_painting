import motor.motor_asyncio
from os import environ

db_name = environ['DB_NAME']
db_host = environ['DB_HOST']

client = motor.motor_asyncio.AsyncIOMotorClient(f'mongodb://{db_host}:27017')
db = client[db_name]
