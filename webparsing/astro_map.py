import requests
from bs4 import BeautifulSoup
import aiohttp


def get_natal_chart_url(year: int, month: int, day: int, hour: int, minutes: int, city: str) -> str:
    url = 'https://geocult.ru/natalnaya-karta-onlayn-raschet?fd='
    url += str(day) + '&fm=' + str(month) + '&fy=' + str(year)
    url += '&fh=' + str(hour) + '&fmn=' + str(minutes)
    url += '&c1=' + city + '%2C+Россия&ttz=20&hs=P&sb=1'
    return url


async def get_natal_chart(year: int, month: int, day: int, hour: int, minutes: int, city: str):
    url = get_natal_chart_url(year, month, day, hour, minutes, city)
    async with aiohttp.ClientSession() as session:
        r = await session.get(url)
        html = await r.text(encoding='UTF-8')

    soup = BeautifulSoup(html, "html.parser")
    images_links = soup.find_all(attrs={'class': 'fancybox'})
    url_links = []
    for images in images_links:
        url_link = images['href']
        url_link = url_link.replace(" ", "%20")
        url_links.append(url_link)
    return url_links
