# 豆瓣读书标签页：https://book.douban.com/tag/
import pandas as pd
from pathlib import Path
import os
import requests
from bs4 import BeautifulSoup


TAG_PAGE_URL = 'https://book.douban.com/tag/'

data_path = Path(__file__).parent.parent / 'data'
try:
    os.mkdir(data_path)
except:
    pass
file_path = data_path / 'tags.csv'


def download_tags():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    resp = requests.get(TAG_PAGE_URL, headers=headers)

    soup = BeautifulSoup(resp.text)
    lst_tags = soup.findAll('td')
    lst_tags = [(e.a.text, e.b.text.lstrip('(').rstrip(')')) for e in lst_tags]
    df = pd.DataFrame(lst_tags, columns=['name', 'id'])
    df.to_csv(file_path, index=False)
    return df


def load_tags():
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print('下载豆瓣读书列表中....')
        return download_tags()


if __name__ == '__main__':
    download_tags()
