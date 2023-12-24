# global imports
import redis.asyncio as redis
from aiogram.fsm.storage.redis import RedisStorage
from dateutil import parser

# local imports
from config_reader import config
from webparsing.horoscope import get_today_horoscope_by_zodiac_sign, get_today_horoscope_by_date

'''
users_data is dict of kind
{ 'id:'+user_id: {sub: int 1/0, sign: str, birth_date: str(datetime.datetime), post_time: str(datetime.time)}}
'''

basic_mapping = {'sub': 0, 'post_time': '11:00', 'sign': 'unknown', 'birth_date': 'unknown'}


storage = redis.Redis(
    host='eu1-enjoyed-deer-40451.upstash.io',
    port=40451,
    password=config.db_password.get_secret_value(),
    decode_responses=True,
)

redis_storage = RedisStorage(storage)


async def get_horoscope_by_id(user_id: int) -> str:
    user_id = 'id:' + str(user_id)
    user_sign = await storage.hget(user_id, key='sign')
    if user_sign is not None:
        return await get_today_horoscope_by_zodiac_sign(user_sign.lower())
    else:
        user_date = await storage.hget(user_id, key='birth_date')
        user_date = parser.parse(user_date)
        return await get_today_horoscope_by_date(user_date.day, user_date.month)
