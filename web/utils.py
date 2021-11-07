import requests
import json
from pathlib import Path
import os


DATA_DIR = Path(__file__).parent.parent / 'data'
IMAGE_PATH = DATA_DIR / 'images'
BOOK_LIST_PATH = DATA_DIR / 'book.json'

if not os.path.exists(IMAGE_PATH):
    os.makedirs(IMAGE_PATH)

# global vars
image_url = None


def get_image_url_mapping():
    global image_url
    if image_url is None:
        with open(BOOK_LIST_PATH, 'r') as f:
            image_url = {i['id']: i['img_url'] for i in json.load(f)}
    return image_url


def get_book_cover_image(book_id):
    image_path = IMAGE_PATH / f'{book_id}.jpg'
    if image_path.exists():
        pass

    url = get_image_url_mapping()[book_id]
    with open(image_path, 'wb') as f:
        f.write(requests.get(url).content)
