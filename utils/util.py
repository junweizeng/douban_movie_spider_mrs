#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/4/3 19:34
# @Author : zjw
# @File : util.py
# @Project : douban_movie_scrapy


def get_movie_id(url):
    # 以https://m.douban.com/movie/subject/1292052/?from=rec 为例，截取从左第39个字符开始到第-10个字符的字符串
    if url[9] == '.' and url[-1] == '/':
        movie_id = url[35:-1]
    elif url[-1] == '/':
        movie_id = url[33:-1]
    elif url[-10:] == '/?from=rec':
        movie_id = url[35:-10]
    elif url[-19:] == '/?from=subject-page':
        movie_id = url[33:-19]
    else:
        movie_id = 'invalid'
    return movie_id
