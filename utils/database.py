#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/28 22:36
# @Author : zjw
# @File : database.py
# @Project : douban_movie_scrapy

"""
    数据库连接
"""

import os

import pymysql

# 映射对象
MYSQL_HOST = os.environ.get("MYSQL_HOST", "rm-xxxxxxxxxxxxx.mysql.rds.aliyuncs.com")
MYSQL_USER = os.environ.get("MYSQL_USER", "xxxxx")
MYSQL_PASS = os.environ.get("MYSQL_PASS", "xxxxx")
MYSQL_DB = os.environ.get("MYSQL_DB", "mrs")

connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    db=MYSQL_DB,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
)
