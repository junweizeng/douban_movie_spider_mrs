#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/4/16 20:27
# @Author : zjw
# @File : db_test.py
# @Project : douban_movie_spider_mrs


import utils.database as db

cursor = db.connection.cursor()

if __name__ == '__main__':
    did = '3256661'
    select_did_sql = "SELECT * FROM movie WHERE did = 5912992"
    cursor.execute(select_did_sql)  # 执行SQL语句
    res = cursor.fetchone()  # 获取执行结果
    if res is not None:
        print(res)
    else:
        print('hello')
