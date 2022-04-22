#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/4/21 19:44
# @Author : zjw
# @File : type_and_region_format.py
# @Project : douban_movie_spider_mrs

"""
    功能说明：
        爬虫抓取的电影信息中，电影类型和地区的格式为（例：‘剧情 / 犯罪'，'中国大陆 / 美国'等)，需要将其拆分后存入数据库中
        电影类型 和 电影地区 需要分别抽取到数据库的movie_type 和 movie_region表中
    数据库说明：
        - movie_type字段：mid（电影id）、tid（类型id）、degree（程度，即该类型在电影中占比）
        - movie_region字段：mid（电影id）、rid（地区id）、degree（程度，即该电影主要是哪个地区的）
"""
import logging

import utils.database as db

cursor = db.connection.cursor()

type_enum = {
    '剧情': 0, '喜剧': 1, '动作': 2,
    '爱情': 3, '科幻': 4, '动画': 5,
    '悬疑': 6, '惊悚': 7, '恐怖': 8,
    '犯罪': 9, '音乐': 10, '歌舞': 11,
    '传记': 12, '历史': 13, '战争': 14,
    '西部': 15, '奇幻': 16, '冒险': 17,
    '灾难': 18, '武侠': 19, '其他': 20
}

region_enum = {
    '中国大陆': 0, '美国': 1, '中国香港': 2, '中国台湾': 3,
    '日本': 4, '韩国': 5, '英国': 6, '法国': 7, '德国': 8,
    '意大利': 9, '西班牙': 10, '印度': 11, '泰国': 12,
    '俄罗斯': 13, '伊朗': 14, '加拿大': 15, '澳大利亚': 16,
    '爱尔兰': 17, '瑞典': 18, '巴西': 19, '丹麦': 20
}


def get_movie_types_and_regions_from_db():
    """
    获取库中所有电影的电影id、电影类型、电影地区信息
    :return:
    """
    try:
        sql = "SELECT id, types, regions From movie"
        cursor.execute(sql)  # 执行SQL语句
        res = cursor.fetchall()  # 获取执行结果
        return res
    except Exception as e:
        logging.error(e)


def save_movie_types_into_db(mid, types):
    """
    将电影所属类型存入数据库中
    :param mid: 电影id
    :param types: 电影类型列表
    :return:
    """
    try:
        for (index, _type) in enumerate(types):
            tid = type_enum.get(_type)
            # 判断如果type_enum中没有键值_type，则不存入数据库中
            if tid is None:
                continue
            sql = 'INSERT INTO movie_type (mid, tid, degree) values(%s)' % '%s, %s, %s'
            cursor.execute(sql, (mid, tid, index))
        db.connection.commit()
    except Exception as e:
        logging.error(e)


def save_movie_regions_into_db(mid, regions):
    """
    将电影所属地区存入数据库中
    :param mid: 电影id
    :param regions: 电影地区列表
    :return:
    """
    try:
        for (index, region) in enumerate(regions):
            rid = region_enum.get(region)
            # 判断如果region_enum中没有键值region，则不存入数据库中
            if rid is None:
                continue
            sql = 'INSERT INTO movie_region (mid, rid, degree) values(%s)' % '%s, %s, %s'
            cursor.execute(sql, (mid, rid, index))
        db.connection.commit()
    except Exception as e:
        logging.error(e)


def save_movie_profile_matrix_into_db(mid, types, regions):
    """
    计算电影的特征信息矩阵，并存入数据库中
    特征信息矩阵 —— 例：0100000100...
        其中：0表示没有这个特征，1表示有这个特征
    :param mid: 电影id
    :param types: 电影类型
    :param regions: 电影地区
    :return:
    """
    try:
        matrix = list('0' * 42)
        print(matrix)
        for t in types:
            tid = type_enum.get(t)
            if tid is not None:
                matrix[tid] = '1'
                print(tid)

        for r in regions:
            rid = region_enum.get(r)
            if rid is not None:
                matrix[rid + 21] = '1'
                print(rid + 21)
        matrix = ''.join(matrix)
        print(matrix)
        sql = 'INSERT INTO movie_feature (mid, matrix) values(%s)' % '%s, %s'
        cursor.execute(sql, (mid, matrix))
        db.connection.commit()
    except Exception as e:
        logging.error(e)


def main():
    movies = get_movie_types_and_regions_from_db()
    for movie in movies:
        mid = movie['id']
        types = movie['types'].split(' / ')
        regions = movie['regions'].split(' / ')
        print(mid)
        print(types)
        print(regions)
        # save_movie_types_into_db(mid, types)
        # save_movie_regions_into_db(mid, regions)
        save_movie_profile_matrix_into_db(mid, types, regions)
        print()


if __name__ == '__main__':
    main()
