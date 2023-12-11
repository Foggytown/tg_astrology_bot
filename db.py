# global imports
import redis.asyncio as redis
from aiogram.fsm.storage.redis import RedisStorage

# local imports
from config_reader import config
'''
in progress
users_data is dict of kind
{ 'id:'+user_id: {sub: int 1/0, sign: str, birth_date: str(datetime) format later}}


'''

basic_mapping = {'sub': 0, 'sign': 'unknown', 'birth_date': 'unknown'}

storage = redis.Redis(
    host='eu1-enjoyed-deer-40451.upstash.io',
    port=40451,
    password=config.db_password.get_secret_value(),
    decode_responses=True,
)

redis_storage = RedisStorage(storage)
