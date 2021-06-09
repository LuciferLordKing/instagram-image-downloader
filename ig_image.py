#!/usr/bin/env python

from urllib3 import PoolManager, ProxyManager
from urllib.request import urlretrieve
from datetime import datetime
from PIL import Image

formats = [
    '.jpg',
    '.png',
    '.gif',
    '.bmp'
]

def getUrl(link):
    proxy_ip = input('proxy [None]: ')
    if proxy_ip != '':
        http = ProxyManager(proxy_ip, maxsize = 10)
    else:
        http = PoolManager()
    r = http.request('GET', link).data.decode('utf-8')
    start = r.find('"display_url":"https://scontent') + 15
    end = r.find('"', start)
    return r[start:end].replace('\\u0026', '&')


def savePic(pic_url, filename):
    if filename == '':
        filename = f'ig_downloaded_pic-{str(datetime.now())}.jpg'
    elif filename[len(filename) - 4:len(filename)] not in formats and filename[len(filename) - 5:len(filename)] != '.jpeg':
        filename += '.jpg'
    urlretrieve(pic_url, filename = filename)
    return filename

if __name__ == '__main__':

    link = input('url of the post: ')
    pic_url = getUrl(link)
    print(pic_url)

    filename = input(f'file name [ig_downloaded_pic-{str(datetime.now())}.jpg]: ')
    filename = savePic(pic_url, filename)

    if input('open saved image [Y/n]: ') == 'Y':
        Image.open(filename).show()
