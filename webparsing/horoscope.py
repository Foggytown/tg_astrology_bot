from bs4 import BeautifulSoup
import requests


def get_url_for_tomorrow_horoscope(zodiac_sign):
    url = 'https://horo.mail.ru/prediction/'
    url += zodiac_sign
    url += '/tomorrow/'
    return url


def get_url_for_today_horoscope(zodiac_sign):
    url = 'https://horo.mail.ru/prediction/'
    url += zodiac_sign
    url += '/today/'
    return url


def get_today_horoscope_by_zodiac_sign(zodiac_sign):
    url = get_url_for_today_horoscope(zodiac_sign)
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('div', attrs={'class': 'article__item article__item_alignment_left article__item_html'})
    return tags[0].text


def get_zodiac_sign_by_date(day, month):
    astro_sign = ''
    if month == 12:
        astro_sign = 'sagittarius' if (day < 22) else 'capricorn'

    elif month == 1:
        astro_sign = 'capricorn' if (day < 20) else 'aquarius'

    elif month == 2:
        astro_sign = 'aquarius' if (day < 19) else 'pisces'

    elif month == 3:
        astro_sign = 'pisces' if (day < 21) else 'aries'

    elif month == 4:
        astro_sign = 'aries' if (day < 20) else 'taurus'

    elif month == 5:
        astro_sign = 'taurus' if (day < 21) else 'gemini'

    elif month == 6:
        astro_sign = 'gemini' if (day < 21) else 'cancer'

    elif month == 7:
        astro_sign = 'cancer' if (day < 23) else 'leo'

    elif month == 8:
        astro_sign = 'leo' if (day < 23) else 'virgo'

    elif month == 9:
        astro_sign = 'virgo' if (day < 23) else 'libra'

    elif month == 10:
        astro_sign = 'libra' if (day < 23) else 'scorpio'

    elif month == 11:
        astro_sign = 'scorpio' if (day < 22) else 'sagittarius'
    return astro_sign


def get_today_horoscope_by_date(day, month):
    zodiac_sign = get_zodiac_sign_by_date(day, month)
    return get_today_horoscope_by_zodiac_sign(zodiac_sign)


sign_to_number = {'Aries': 1, 'Taurus': 2, 'Gemini': 3,
                  'Cancer': 4, 'Leo': 5, 'Virgo': 6,
                  'Libra': 7, 'Scorpio': 8, 'Sagittarius': 9,
                  'Capricorn': 10, 'Aquarius': 11, 'Pisces': 12}


def get_compatibility_url(id):
    url = 'https://horo.mail.ru/compatibility/zodiac/'
    url += str(id)
    url += '/'
    return url


def get_compatibility_zodiac(woman, man):
    id = (sign_to_number[woman] - 1) * 12 + sign_to_number[man]
    url = get_compatibility_url(id)
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    tags_image = soup.find_all('div', attrs={'class': 'p-item__left'})

    tags_text = soup.find_all('div', attrs={'class': 'article__item article__item_alignment_left article__item_html'})

    return tags_image[0].text.strip() + '\n' + tags_text[0].text.strip()
