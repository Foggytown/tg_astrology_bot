from aiogram import Router, F
from aiogram.filters import Command
from aiogram import types
from aiogram.filters import CommandObject
from dateutil import parser

router = Router()


# Хэндлер на команду /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Здравствуйте, вас приветствует бот для ежедневных гороскопов и натальных карт,"
                         + "пожалуйста введите свою дату рождения ниже в формате: \n/date 17.05.2004")


@router.message(Command("date"))
async def cmd_name(message: types.Message, command: CommandObject):
    try:
        print(message.text)
        date=parser.parse(message.text.split()[1])
        await message.answer(str(date.day))

    except parser._parser.ParserError as error:
        await message.answer('Вы неправильно указали дату своего рождения, укажите ее в формате\n/date 17.05.2004')




@router.message(Command('images'))
async def upload_photo(message: types.Message):
    file_ids = []

    image_from_url = types.URLInputFile("https://cdn130.picsart.com/266356863020202.png?to=crop&type=webp&r=1456x1456&q=85")
    result = await message.answer_photo(
        image_from_url,
        caption="Изображение по ссылке"
    )
    file_ids.append(result.photo[-1].file_id)
    await message.answer("Отправленные файлы:\n"+"\n".join(file_ids))
