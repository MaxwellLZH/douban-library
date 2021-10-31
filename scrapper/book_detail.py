from pathlib import Path
import os
import json
import requests
from bs4 import BeautifulSoup

data_path = Path(__file__).parent.parent / 'data'
try:
    os.mkdir(data_path)
except:
    pass
book_list_path = data_path / 'books.json'
file_path = data_path / 'book_detail.json'


url = 'https://book.douban.com/subject/4167565/'


def get_single_book_detail(d: dict):
    url = d['url']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text)
    div_info = soup.find('div', id='info')
    intro = soup.find('div', class_='intro').get_text().strip()
    detail = {'info_html': str(div_info), 'intro': intro}
    return {**d, **detail}


with open(book_list_path, 'r') as f:
    lst_books = json.load(f)

