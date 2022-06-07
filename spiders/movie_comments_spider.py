#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/5/1 10:57
# @Author : zjw
# @File : movie_comments_spider.py
# @Project : douban_movie_spider_mrs
import logging

from lxml import etree

import requests
import time
from datetime import datetime
from fake_useragent import UserAgent

from movie_info_spider import get_response
import utils.database as db

cursor = db.connection.cursor()


def save_user_into_db(user):
    try:
        isExists = get_user_id_from_db(user['username'])
        if isExists is None:
            now = time.time()
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))
            user['sex'] = 2
            user['create_time'] = now
            values = tuple(user.values())
            new_values = ','.join(["%s"] * len(values))
            insert_info_sql = "insert into user (username, nickname, avatar, sex, create_time) values (%s)" % new_values
            cursor.execute(insert_info_sql, values)
            db.connection.commit()
    except Exception as e:
        logging.error(e)


def get_user_id_from_db(username):
    try:
        select_did_sql = "SELECT id FROM user WHERE username = '%s'" % username
        cursor.execute(select_did_sql)  # 执行SQL语句
        res = cursor.fetchone()         # 获取执行结果
        return res
    except Exception as e:
        logging.error(e)


def get_movie_id_from_db(did):
    try:
        select_did_sql = "SELECT id FROM movie WHERE did = '%s'" % did
        cursor.execute(select_did_sql)  # 执行SQL语句
        res = cursor.fetchone()         # 获取执行结果
        return res
    except Exception as e:
        logging.error(e)


def get_all_movie_did_from_db():
    try:
        sql = "SELECT did FROM movie m WHERE m.id NOT IN (SELECT DISTINCT mid FROM `comment`)"
        cursor.execute(sql)             # 执行SQL语句
        res = cursor.fetchall()         # 获取执行结果
        return res
    except Exception as e:
        logging.error(e)


def save_movie_comments_into_db(comment):
    user_id = get_user_id_from_db(comment['username'])
    movie_id = get_movie_id_from_db(comment['mid'])
    insert_comment = {'uid': user_id['id'], 'mid': movie_id['id'], 'comment': comment['comment'], 'score': comment['score'],
                      'time': comment['time'], 'agree': comment['agree'], 'type': 1, 'nickname': comment['nickname']}
    try:
        values = tuple(insert_comment.values())
        new_values = ','.join(["%s"] * len(values))
        insert_comment_sql = "insert into comment (uid, mid, comment, score, time, agree, type, nickname) values (%s)" % new_values
        print(insert_comment_sql)
        print(values)
        cursor.execute(insert_comment_sql, values)
        db.connection.commit()
    except Exception as e:
        logging.error(e)


def format_comment_info(info):
    if info and len(info):
        info = [i.strip() for i in info]
    else:
        info = []
    return info


def get_score_num(score):
    if score == '力荐':
        score = 10
    elif score == '推荐':
        score = 8
    elif score == '还行':
        score = 6
    elif score == '较差':
        score = 4
    elif score == '很差':
        score = 2
    else:
        score = 0
    return score


def get_and_save_movie_comments(mid, response):
    try:
        response = etree.HTML(response.text)
        comments = {}
        comment_regex = '//*[@id="comments"]/div/div[2]/p/span/text()'
        username_regex = '//*[@id="comments"]/div/div["comment-info"]/a/@href'
        nickname_regex = '//*[@id="comments"]/div/div[2]/h3/span[2]/a/text()'
        avatar_regex = '//*[@id="comments"]/div/div[1]/a/img/@src'
        score_regex = '//*[@id="comments"]/div/div[2]/h3/span[2]/span[2]/@title'
        time_regex = '//*[@id="comments"]/div/div[2]/h3/span[2]/span[3]/text()'
        agree_regex = '//*[@id="comments"]/div/div[2]/h3/span[1]/span/text()'

        comment = response.xpath(comment_regex)
        comment = format_comment_info(comment)

        username = response.xpath(username_regex)
        username = format_comment_info(username)
        username = [u[30:-1] for u in username]

        nickname = response.xpath(nickname_regex)
        nickname = format_comment_info(nickname)

        avatar = response.xpath(avatar_regex)
        avatar = format_comment_info(avatar)

        score = response.xpath(score_regex)
        score = format_comment_info(score)
        score = [get_score_num(s) for s in score]

        times = response.xpath(time_regex)
        times = format_comment_info(times)

        agree = response.xpath(agree_regex)
        agree = format_comment_info(agree)

        for i in range(len(comment)):
            comment_one = {
                "mid": mid,
                "username": username[i],
                "nickname": nickname[i],
                "avatar": avatar[i],
                "comment": comment[i],
                "score": score[i],
                "time": times[i],
                "agree": agree[i]
            }
            user_one = {
                "username": username[i],
                "nickname": nickname[i],
                "avatar": avatar[i]
            }
            print(user_one)
            save_user_into_db(user_one)
            print(comment_one)
            save_movie_comments_into_db(comment_one)
            print()
    except Exception as e:
        logging.error(e)


def main():
    all_movie_did = get_all_movie_did_from_db()
    print(all_movie_did)
    # i = 0
    for movie in all_movie_did:
        # if movie['id'] == 6311260:
        #     print('idx:' + str(i))
        # i += 1
        print('Movie_Did is ' + str(movie['did']))
        url = 'https://movie.douban.com/subject/' + str(movie['did']) + '/comments?limit=20&status=P&sort=new_score'
        print(url)
        response = get_response(url)
        # 使用XPath解析界面，并将每条评价信息记录存储到数据库中
        get_and_save_movie_comments(movie['did'], response)


if __name__ == '__main__':
    main()
