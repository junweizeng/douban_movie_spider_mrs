#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/4/9 19:58
# @Author : zjw
# @File : aliyun_oss_test.py
# @Project : douban_movie_scrapy

import oss2
import os


def GetFileName(folder):
    file_list = []
    for file in os.listdir(folder):  # 获取当前目录下文件(不带后缀)的名称
        file_list.append(file)
    return file_list


def upload_picture(file_list, folder):
    # 填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
    endpoint = 'https://oss-cn-hangzhou.aliyuncs.com'

    # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
    access_key_id = 'xxxxxx'
    access_key_secret = 'xxxxxx'
    # 填写Bucket名称，例如examplebucket。
    bucket_name = 'mrs-zjw'
    # 指定图片所在Bucket的名称。如果图片不在Bucket根目录，需携带文件完整路径，例如exampledir/example.jpg。
    key = 'mrs/movie/'

    # 指定Bucket实例，所有文件相关的方法都需要通过Bucket实例来调用。
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

    for file in file_list:
        print(key + file)
        print(folder + file)
        # 如果图片不在指定Bucket内，需将该图片到目标Bucket。
        bucket.put_object_from_file(key + file, folder + file)


if __name__ == '__main__':
    folder = 'G:\\Graduation_Design\\mrs_storage\\movie\\'
    li = GetFileName(folder)
    upload_picture(li, folder)
