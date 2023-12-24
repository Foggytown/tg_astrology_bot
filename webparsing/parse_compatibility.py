# global imports
from bs4 import BeautifulSoup
import aiohttp

# local imports
from utils.util_data import sign_to_number


def get_compatibility_url(signs_num: int) -> str:
    url = 'https://horo.mail.ru/compatibility/zodiac/'
    url += str(signs_num)
    url += '/'
    return url


async def get_compatibility_zodiac(woman_sign: int, man_sign: int) -> str:
    signs_num = (sign_to_number[woman_sign] - 1) * 12 + sign_to_number[man_sign]
    url = get_compatibility_url(signs_num)

    async with aiohttp.ClientSession() as session:
        r = await session.get(url)
        html = await r.text(encoding='UTF-8')

    soup = BeautifulSoup(html, "html.parser")

    tags_image = soup.find_all('div', attrs={'class': 'p-item__left'})

    tags_text = soup.find_all('div', attrs={'class': 'article__item article__item_alignment_left article__item_html'})

    return tags_image[0].text.strip() + '\n' + tags_text[0].text.strip()
