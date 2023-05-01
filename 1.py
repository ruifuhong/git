import pandas as pd
from bs4 import BeautifulSoup
import json
import requests
import re

keyword = '刷毛外套'
pages = 15
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
urls = []
for page in range(1, pages):
    url = 'https://m.momoshop.com.tw/search.momo?_advFirst=N&_advCp=N&curPage={}&searchType=1&cateLevel=2&ent=k&searchKeyword={}&_advThreeHours=N&_isFuzzy=0&_imgSH=fourCardType'.format(page, keyword)
    print(url)
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text)
        for item in soup.select('li.goodsItemLi > a'):
            urls.append('https://m.momoshop.com.tw'+item['href'])
    urls = list(set(urls))
    print(len(urls))
#     break