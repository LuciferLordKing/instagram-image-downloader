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

class IgPost:

    def __init__(self, link):
        self._link = link

    def setProxy(self, proxy_ip):
        if proxy_ip != '':
            self._http = ProxyManager(proxy_ip, maxsize = 10)
        else:
            self._http = PoolManager()

    def getPicUrl(self):
        r = self._http.request('GET', self._link).data.decode('utf-8')
        start = r.find('"display_url":"https://scontent') + 15
        end = r.find('"', start)
        return r[start:end].replace('\\u0026', '&')

class Pic:

    def __init__(self, pic_url, filename):
        self._pic_url = pic_url
        if filename == '':
            self._filename = f'ig_downloaded_pic-{str(datetime.now())}.jpg'
        elif filename[len(filename) - 4:len(filename)] not in formats and self._filename[len(filename) - 5:len(filename)] != '.jpeg':
            self._filename = filename + '.jpg'
        else:
            self._filename = filename

    def savePic(self):
        urlretrieve(self._pic_url, filename = self._filename)

    def openPic(self):
        if input('open saved image [Y/n]: ') == 'Y':
            Image.open(self._filename).show()

if __name__ == '__main__':

    ig_post = IgPost(input('url of the post: '))
    ig_post.setProxy(input('proxy [None]: '))
    print(ig_post.getPicUrl())

    pic = Pic(ig_post.getPicUrl(), input(
        f'file name [ig_downloaded_pic-{str(datetime.now())}.jpg]: '))
    pic.savePic()
    pic.openPic()
