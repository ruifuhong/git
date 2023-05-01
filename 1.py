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

df = []
for i, url in enumerate(urls):
    columns = []
    values = []
    
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text)
    # 標題
    title = soup.find('meta',{'property':'og:title'})['content']
    # 品牌
    #brand = soup.find('meta',{'property':'product:brand'})['content']
    # 連結
    #link = soup.find('meta',{'property':'og:url'})['content']
    # 原價
    try:
        price = re.sub(r'\r\n| ','',soup.find('del').text)
    except:
        price = ''
    # 特價
    amount = soup.find('meta',{'property':'product:price:amount'})['content']
    # 類型
    cate = ''.join([i.text for i in soup.findAll('article',{'class':'pathArea'})])
    cate = re.sub('\n|\xa0',' ',cate)
    # 描述
    #try:
        #desc = soup.find('div',{'class':'Area101'}).text
        #desc = re.sub('\r|\n| ', '', desc)
    #except:
        #desc = ''
    
    print('==================  {}  =================='.format(i))    
    print(title)
    #print(brand)
    #print(link)
    print(amount)
    print(cate)
    
    columns += ['title', 'price', 'amount', 'cate']
    values += [title, price, amount, cate]

    # 規格
    for i in soup.select('div.attributesArea > table > tr'):
        try:
            column = i.find('th').text
            column = re.sub('\n|\r| ','',column)
            if column not in ["顏色", "尺寸"]:
                continue
            value = ''.join([j.text for j in i.findAll('li')])
            value = re.sub('\n|\r| ','',value)
            columns.append(column)
            values.append(value)
        except:
            pass
    ndf = pd.DataFrame(data=values, index=columns).T
    df.append(ndf)
df=pd.concat(df, ignore_index=True)

df.info()

df.to_excel('./MOMO.xlsx')