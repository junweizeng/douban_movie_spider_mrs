#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/4/29 20:29
# @Author : zjw
# @File : time_random_test.py
# @Project : douban_movie_spider_mrs
import random
import time


if __name__ == '__main__':
    x = random.random() * 3
    print(x)
    time.sleep(random.random() * 3)
    print(1)
