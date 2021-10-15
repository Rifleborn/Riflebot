import requests
from bs4 import BeautifulSoup
from config import settings

# URL our site what we need to parse
URL = settings['URL']
# imitating browser work (not bot activity)
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
# host from site's URL
HOST = settings['HOST']


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_=settings['CONTENT_CLASS'])

    cars = []
    for item in items:
        uah_price = item.find('span', class_='size15')
        if uah_price:
            uah_price = uah_price.get_text().replace(' • ', '')
        else:
            uah_price = 'Цену уточняйте'
        cars.append({
            'title': item.find('div', class_='na-card-name').get_text(strip=True),
            'link': HOST + item.find('span', class_='link').get('href'),
            'usd_price': item.find('strong', class_='green').get_text(),
            'uah_price': uah_price,
            'city': item.find('svg', class_='svg_i16_pin').find_next('span').get_text(),
        })
    return cars


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = get_content(html.text)
    else:
        print('Error')


parse()
