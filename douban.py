import random
from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
import time


base_url = 'https://m.douban.com/rexxar/api/v2/gallery/topic/17769/items?'

headers = {
'Referer': 'https://www.douban.com/gallery/topic/17769/?dt_dapp=1',
'User-Agent':'User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
}
# user_agent_list = [
#     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
#     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
#     "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
#     ]
# headers['User-Agent'] = random.choice(user_agent_list)


def get_page(page):
    params = {
        'from_web': '1',
        'sort': 'hot',
        'start': page,
        'count': '20',
        'status_full_tex': '1',
        'guest_only': '0',
        'ck': 'null'
    }
    url = base_url + urlencode(params)
    print(url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)



def parse_page(json):
    if json:
        items = json.get('items')
        for item in items:
            item = item.get('target')
            douban = {}
            try:
                douban['author'] = item.get('status').get('author').get('name')
            except AttributeError:
                douban['author'] = 'null'

            try:
                douban['address'] = item.get('status').get('author').get('loc').get('name')
            except AttributeError:
                douban['address'] = 'null'

            try:
                douban['douban_url'] = item.get('status').get('author').get('url')
            except AttributeError:
                douban['douban_url'] = 'null'

            try:
                douban['text'] = item.get('status').get('text').replace('\n', '').replace('\r', '')
            except AttributeError:
                douban['text'] = 'null'
            yield douban

if __name__ == '__main__':
    for page in range(0, 500, 20):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            print(result)
        time.sleep(10)