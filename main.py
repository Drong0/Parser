import requests
from bs4 import BeautifulSoup
import json

URL = 'https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/'

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',

    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 '
                  'Safari/537.36 OPR/93.0.0.0'
}


def get_html(url, params='', headers=None):
    if headers is None:
        headers = HEADERS
    r = requests.get(url, headers=headers, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_='gtm-impression-product')
    smartphones = []
    for item in items:
        data_string = item['data-product']
        data_json = json.loads(data_string)
        articul = data_json['item_id']
        name = data_json['item_name']
        price = data_json['price']
        memory_size = name.split(',')[1].strip().split(' ')[0]
        smartphones.append({
            'articul': articul,
            'name': name,
            'price': price,
            'memory_size': memory_size
        })
    return smartphones


def parser():
    PAGE = 14
    html = get_html(URL)
    if html.status_code == 200:
        smartphones = []
        for page in range(1, PAGE):
            html = get_html(URL, params={'PAGEN_1': page})
            smartphones.extend(get_content(html.text))
        print(f'Получено {len(smartphones)} смартфонов')
        with open('smartphones.json', 'w', encoding='utf-8') as file:
            json.dump(smartphones, file, indent=4, ensure_ascii=False)


parser()
