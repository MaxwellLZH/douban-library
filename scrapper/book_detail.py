from pathlib import Path
import os
import json
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()

data_path = Path(__file__).parent.parent / 'data'
try:
    os.mkdir(data_path)
except:
    pass
book_list_path = data_path / 'books.json'
file_path = data_path / 'book_detail.json'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Host': 'book.douban.com',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'macOS',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'sec-gpc': '1',
    'Upgrade-Insecure-Requests': '1',
}

def get_single_book_detail(d: dict):
    url = d['url']
    resp = requests.get(url, headers=headers)
    print(resp.text)
    soup = BeautifulSoup(resp.text)
    div_info = soup.find('div', id='info')
    # 简介
    intro = soup.find('div', class_='intro').text.strip()
    # 短评
    div_comment = soup.find('div', id='comment-list-wrapper')
    lst_comment = [i.text.strip() for i in div_comment.findAll('p', class_='comment-content')]
    detail = {'info_html': str(div_info), 'intro': intro, 'short_comment': lst_comment}
    return {**d, **detail}


with open(book_list_path, 'r') as f:
    lst_books = json.load(f)

# https://book.douban.com/subject/27614904/

book = lst_books[2]
print(book)
print(get_single_book_detail(book)['info_html'])
