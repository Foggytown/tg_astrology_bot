from aiogram.filters import BaseFilter
from aiogram.types import Message
from config_reader import config


class IsDeveloper(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) in [config.developer_id1.get_secret_value(),
                                             config.developer_id2.get_secret_value()]
