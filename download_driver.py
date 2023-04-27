import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
from tqdm import  *

header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9, en; q = 0.8, en - GB; q = 0.7, en - US; q = 0.6"
    }
url=r'https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/'
request=requests.get(url,headers=header)
html=request.text
soup=BeautifulSoup(html,'lxml')

a=soup.select('div.module')[2]
download_url=a.select('a')[1]['href']
download_zip=requests.get(download_url,stream=True)
total=int(download_zip.headers['Content-Length'])

try:
    with open('driver.zip','wb') as file, tqdm(
            desc=f'正在下载',
            total=total,
            unit='B',
            unit_scale=True,
            ncols=100,
            colour='#00ff00',  # 进度条颜色 仅编辑器内有效
    )  as bar:
        for code in download_zip.iter_content(1024):
            size=file.write(code)
            bar.update(size)
    download_res=True
    print('It has been downloaded')
except Exception as e:
    download_res = False
    print(f'Download failed : {e}')

if download_res:
    try:
        with ZipFile('driver.zip','r') as zipf:
            zipf.extractall()
            res=True
            print('It has been decompressed')
    except Exception as e:
        res = False
        print(f'Decompression failed : {e}')
    if res: os.remove('driver.zip')
