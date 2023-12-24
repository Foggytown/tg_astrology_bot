# global imports
from bs4 import BeautifulSoup
import aiohttp

# local imports
from utils.util_funcs import get_zodiac_sign_by_date


def get_url_for_tomorrow_horoscope(zodiac_sign: str) -> str:
    url = 'https://horo.mail.ru/prediction/'
    url += zodiac_sign
    url += '/tomorrow/'
    return url


def get_url_for_today_horoscope(zodiac_sign: str) -> str:
    url = 'https://horo.mail.ru/prediction/'
    url += zodiac_sign
    url += '/today/'
    return url


async def get_today_horoscope_by_zodiac_sign(zodiac_sign: str) -> str:
    url = get_url_for_today_horoscope(zodiac_sign)
    async with aiohttp.ClientSession() as session:
        r = await session.get(url)
        html = await r.text(encoding='UTF-8')

    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('div', attrs={'class': 'article__item article__item_alignment_left article__item_html'})
    return tags[0].text


async def get_today_horoscope_by_date(day: int, month: int) -> str:
    zodiac_sign = get_zodiac_sign_by_date(day, month)
    return await get_today_horoscope_by_zodiac_sign(zodiac_sign)
