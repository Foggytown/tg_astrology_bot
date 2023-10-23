import redis.asyncio as redis
import json
import pickle

users_data = []
'''
future plans
users_data is dict of kind
{user_id: {is_sub: bool, sign: str, date_of_birth: datetime or smth}}

now
users_data is list of subed users

'''

storage = redis.Redis(
    host='eu1-enjoyed-deer-40451.upstash.io',
    port=40451,
    password='2315b6d835d74b5a9f0201b0e841bbdb',
)


async def load_db():
    global storage, users_data

    users_data = []
    res = await storage.get('users_data')
    if res:
        users_data = json.loads(res)
        print(users_data, 'load_db')


async def get_db():
    global users_data
    return users_data


async def save_db():
    global storage, users_data
    print(users_data, 'save_db')
    res = json.dumps(users_data)
    print(bool(res), 'save_db')
    if res:
        await storage.set('users_data', res)
    else:
        await storage.delete('users_data')
