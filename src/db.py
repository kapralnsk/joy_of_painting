import motor.motor_asyncio
from os import environ

db_name = environ['DB_NAME']

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://db:27017')
db = client[db_name]
