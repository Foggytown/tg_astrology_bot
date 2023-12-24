# global imports
from aiogram import Router
from aiogram.filters import Command
from aiogram import types
from dateutil import parser

# local imports
from db import storage, basic_mapping

router = Router()

# !!!!!!!!!!!!!!!! DEPRECATED
# only for testing purposes
# now just turned off, just legacy code


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = 'id:' + str(message.from_user.id)
    if (await storage.hgetall(user_id)) == {}:
        await storage.hset(user_id, mapping=basic_mapping)
        await message.answer("Здравствуйте, вас приветствует бот для ежедневных гороскопов и натальных карт,"
                             + "пожалуйста введите свою дату рождения ниже в формате: \n/date 17.05.2004")
    else:
        await message.answer("Мы с вами уже знакомы.")


@router.message(Command("subscribe"))
async def cmd_sub(message: types.Message):
    user_id = 'id:' + str(message.from_user.id)
    user_subbed = await storage.hget(user_id, 'sub')
    if int(user_subbed):
        await message.answer("Вы уже подписаны на рассылку гороскопов.")
    else:
        await storage.hset(user_id, mapping={'sub': 1})
        await message.answer("Спасибо, вы подписались на ежедневную рассылку гороскопов.")


@router.message(Command("unsubscribe"))
async def cmd_unsub(message: types.Message):
    user_id = 'id:' + str(message.from_user.id)
    user_subbed = await storage.hget(user_id, 'sub')
    if int(user_subbed):
        await storage.hset(user_id, mapping={'sub': 0})
        await message.answer("Вы были отписаны от рассылки.")
    else:
        await message.answer("Вы и так не подписаны на рассылку.")


@router.message(Command("clear_data"))
async def cmd_delete(message: types.Message):
    user_id = 'id:' + str(message.from_user.id)
    await storage.delete(user_id)


@router.message(Command("date"))
async def cmd_date(message: types.Message):
    user_id = 'id:' + str(message.from_user.id)
    user_subbed = await storage.hget(user_id, 'sub')
    try:
        print(message.text)
        date = parser.parse(message.text.split()[1])
        await message.answer(str(date.day))

    except parser._parser.ParserError as error:
        await message.answer('Вы неправильно указали дату своего рождения, укажите ее в формате\n/date 17.05.2004')


@router.message(Command('images'))
async def upload_photo(message: types.Message):
    file_ids = []

    image_from_url = types.URLInputFile(
        "https://cdn130.picsart.com/266356863020202.png?to=crop&type=webp&r=1456x1456&q=85")
    result = await message.answer_photo(
        image_from_url,
        caption="Изображение по ссылке"
    )
    file_ids.append(result.photo[-1].file_id)
    await message.answer("Отправленные файлы:\n" + "\n".join(file_ids))
