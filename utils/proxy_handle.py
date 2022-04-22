#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/30 12:18
# @Author : zjw
# @File : proxy_handle.py
# @Project : douban_movie_scrapy
import json

import requests


def get_five_proxy():
    url = 'http://http2.9vps.com/getip.asp?username=401022254&pwd=d52c3b' \
          '42879274361afe984dc0c8f142&geshi=1&fenge=1&fengefu=&getnum=5'

    response = requests.get(url)
    html = response.text
    urls = html.split('\r\n')
    return urls


def get_proxy():
    import time
    time.sleep(1)
    url = 'http://http.9vps.com/getip.asp?username=401022254&pwd=d52c3b42879274361afe984dc0c8f142&geshi=1&fenge=1&fengefu=&getnum=1'
    response = requests.get(url)
    return response.text


if __name__ == '__main__':
    print(get_proxy())
