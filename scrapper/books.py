# 豆瓣读书指定标签下书籍列表：https://book.douban.com/tag/{tag_name}?start=40&type=T
import requests
from bs4 import BeautifulSoup
from typing import *
from pathlib import Path
import os
import json
import itertools
from concurrent.futures import ThreadPoolExecutor

from scrapper.tags import load_tags


BOOK_LIST_URL = 'https://book.douban.com/tag/{tag_name}?start={start}&type=T'

data_path = Path(__file__).parent.parent / 'data'
try:
    os.mkdir(data_path)
except:
    pass
file_path = data_path / 'books.json'


def get_books_from_single_page(page_url: str) -> List[dict]:
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    resp = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(resp.text)
    lst_books = soup.findAll('li', class_='subject-item')

    def _extract(e):
        div_info = e.find('div', class_='info')
        name = div_info.a.attrs['title'].strip()
        url = div_info.a.attrs['href']
        id = int(url.split(r'/subject/')[1].rstrip(r'/'))
        img_url = e.img.attrs['src']

        try:
            rating = float(e.find('span', class_='rating_nums').text.strip())
        except:
            rating = -1.0

        try:
            short_desc = e.find('p').text.strip()
        except AttributeError:
            short_desc = ''
        return {'id': id, 'name': name, 'url': url, 'img_url': img_url,
                'rating': rating, 'short_desc': short_desc, 'from_url': page_url}
    lst_books = [
            _extract(e) for e in lst_books
        ]
    print('Successfully get book list from:', page_url)
    return lst_books


if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        lst_books = json.load(f)
        seen_url = set([i['from_url'] for i in lst_books])
else:
    lst_books, seen_url = [], set()


df_tags = load_tags()
tags = df_tags['name']

urls = []
for tag, start in itertools.product(tags, list(range(0, 1020, 20))):
    url = BOOK_LIST_URL.format(tag_name=tag, start=start)
    if url not in seen_url:
        urls.append(url)

print('Number of URLs to scrap: {}'.format(len(urls)))

with ThreadPoolExecutor(max_workers=20) as ex:
    res = list(ex.map(get_books_from_single_page, urls[:2000]))

for r in res:
    lst_books.extend(r)

with open(file_path, 'w', encoding='utf8') as f:
    json.dump(lst_books, f)

