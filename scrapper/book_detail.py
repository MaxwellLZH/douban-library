from pathlib import Path
import os
import json
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor

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
    resp = requests.get(url, headers=headers, allow_redirects=False)
    soup = BeautifulSoup(resp.text)
    # 基本信息
    div_info = soup.find('div', id='info')
    lst_info = list(div_info.stripped_strings)
    dict_info = {}

    seen_key, key, value = False, None, None
    for i in lst_info:
        if not seen_key:
            key = i.replace(':', '')
            seen_key = True
        else:
            if i.strip() == ':':
                continue
            else:
                value = i.strip()
                dict_info[key] = value
                seen_key, key, value = False, None, None

    # for i in range(len(lst_info) // 2):
    #     dict_info[lst_info[2 * i].rstrip(':')] = lst_info[2 * i +1]

    print(lst_info)
    print(dict_info)

    # 简介
    intro = soup.find('div', class_='intro').text.strip()
    # 短评
    div_comment = soup.find('div', id='comment-list-wrapper')
    lst_comment = [i.text.strip() for i in div_comment.findAll('p', class_='comment-content')]
    detail = {'info_html': str(div_info),
              'intro': intro,
              'short_comment': lst_comment}
    detail.update(**dict_info)
    print('Successfully downloaded book:', d['name'])
    return {**d, **detail}


d = {'url': 'https://book.douban.com/subject/4913064/', 'name': 'x'}
print(get_single_book_detail(d))


#
# with open(book_list_path, 'r') as f:
#     lst_books = json.load(f)
# lst_id = [i['id'] for i in lst_books]
#
#
# if os.path.exists(file_path):
#     with open(file_path, 'w') as f:
#         lst_book_detail = json.load(f)
#         downloaded_id = set([i['id'] for i in lst_book_detail])
# else:
#     downloaded_id = set()
#     lst_book_detail = []
#
# tasks = [b for b in lst_books if b['id'] not in downloaded_id]
# print('Remaining task count:', len(tasks))
#
#
# with ThreadPoolExecutor(max_workers=20) as ex:
#     res = list(ex.map(get_single_book_detail, tasks[:100]))
#
# lst_book_detail.extend(res)
#
# with open(file_path, 'w') as f:
#     json.dump(lst_book_detail, f)
