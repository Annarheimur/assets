# -*- coding:UTF-8 -*-
import requests
import re
import base64
import time
from bs4 import BeautifulSoup

def getNoteInfo( link ):
    # 获取jd信息
    print(link)
    content = requests.get(url=link)
    pattern = r'([vmes]{2,5}:\/\/[^<]{10,})'
    result = re.findall(pattern, content.text, re.M)
    return result

if __name__ == '__main__':
    # 获取详情页链接
    target = 'https://www.mattkaydiary.com/'
    req = requests.get(url=target)
    soup = BeautifulSoup(req.text, "html5lib").select('.post-title > a')
    result = []

    for link in soup:
      if(len(result) == 0):
        result = getNoteInfo(link.get('href'))
      else:
        break

    # 写入文件
    result = '\n'.join(result)
    result = str(base64.b64encode(result.encode('utf-8')),"utf-8")
    filename = time.strftime("%Y-%m-%d", time.localtime())
    with open('otw/'+filename + '.js', 'w') as f:
      f.write(result)

    s = requests.session()
    s.keep_alive = False

    # 刷新CDN
    cdnLink = 'https://purge.jsdelivr.net/gh/annarheimur/assets/otw/'+filename+'.js'
    cdnResp = requests.get(cdnLink)
    print('文件生成成功',cdnLink, cdnResp.text)
