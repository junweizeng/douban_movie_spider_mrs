#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/4/16 15:03
# @Author : zjw
# @File : main.py
# @Project : douban_movie_scrapy
import random

from fake_useragent import UserAgent
from lxml import etree
import requests
import json
import time
import uuid
import logging
from datetime import datetime

from utils.proxy_handle import get_proxy
from utils.util import get_movie_id
import utils.database as db


PUBLIC_PROXY = get_proxy()

cursor = db.connection.cursor()


def get_movie_urls(page_start):
    """
    获取每部电影详情的url地址
    :param page_start: 起始号
    :return: 电影url列表
    """
    movies_did_url = \
        'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=' + str(page_start)
    response = get_response(movies_did_url)
    json_text = json.loads(response.text)
    subjects = json_text['data']
    movie_urls = []
    for subject in subjects:
        movie_urls.append(subject['url'])
    return movie_urls


def get_movie_info(response):
    """
    爬取电影详情界面每个字段的具体信息
    :param response: 电影详情页面响应
    :return: 电影详情对象
    """
    did = get_movie_id(response.url)
    print('did:' + did)

    response = etree.HTML(response.text)
    info = {}

    name_regex = "//title/text()"
    name = response.xpath(name_regex)
    if name and len(name):
        name = name[0][:-5].strip()
        print('name:' + name)
    else:
        name = ''

    year_regex = '//span[@class="year"]/text()'
    year = response.xpath(year_regex)
    if year and len(year):
        year = year[0][1:-1].strip()
        print('year:' + year)
    else:
        year = ''

    directors_regex = '//a[@rel="v:directedBy"]/text()'
    directors = response.xpath(directors_regex)
    if directors and len(directors):
        directors = " / ".join(directors[:])
        print('director:' + directors)
    else:
        directors = ''

    writers_regex = '//span[preceding-sibling::span[text()="编剧"]]/a/text()'
    writers = response.xpath(writers_regex)
    if writers and len(writers):
        writers = " / ".join(writers)
        print('writers:' + writers)
    else:
        writers = ''

    actors_regex = '//a[@rel="v:starring"]/text()'
    actors = response.xpath(actors_regex)
    if actors and len(actors):
        actors = " / ".join(actors)
        print('actors:' + actors)
    else:
        actors = ''

    types_regex = '//span[@property="v:genre"]/text()'
    types = response.xpath(types_regex)
    if types and len(types):
        types = " / ".join(types)
        print('types:' + types)
    else:
        types = ''

    regions_regex = '//text()[preceding-sibling::span[text()="制片国家/地区:"]]'
    regions = response.xpath(regions_regex)
    if regions and len(regions):
        # regions = '/'.join(regions[0].strip().split(' / '))
        regions = regions[0].strip()
        print('regions:' + regions)
    else:
        regions = ''

    languages_regex = '//text()[preceding-sibling::span[text()="语言:"]]'
    languages = response.xpath(languages_regex)
    if languages and len(languages):
        # languages = '/'.join(languages[0].strip().split(' / '))
        languages = languages[0].strip()
        print('languages:' + languages)
    else:
        languages = ''

    release_date_regex = '//span[@property="v:initialReleaseDate"]/text()'
    release_date = response.xpath(release_date_regex)
    if release_date and len(release_date):
        release_date = " / ".join(release_date)
        print('release_date:' + release_date)
    else:
        release_date = ''

    runtime_regex = '//span[@property="v:runtime"]/text()'
    runtime = response.xpath(runtime_regex)
    if runtime and len(runtime):
        runtime = runtime[0][:-2].strip()
        print('runtime:' + runtime)
    else:
        runtime = ''

    alias_regex = '//text()[preceding-sibling::span[text()="又名:"]]'
    alias = response.xpath(alias_regex)
    if alias and len(alias):
        # alias = '/'.join(alias[0].strip().split(' / '))
        alias = alias[0].strip()
        print('alias:' + alias)
    else:
        alias = ''

    imdb_regex = '//text()[preceding-sibling::span[text()="IMDb:"]]'
    imdb = response.xpath(imdb_regex)
    if imdb and len(imdb):
        imdb = imdb[0].strip()
        print('imdb:' + imdb)
    else:
        imdb = ''

    score_regex = '//strong[@property="v:average"]/text()'
    score = response.xpath(score_regex)
    if score and len(score):
        score = score[0].strip()
        print('score:' + score)
    else:
        score = '0'

    num_regex = '//span[@property="v:votes"]/text()'
    num = response.xpath(num_regex)
    if num and len(num):
        num = num[0].strip()
        print('score:' + num)
    else:
        num = '0'

    percentages_regex = '//span[@class="rating_per"]/text()'
    percentages = response.xpath(percentages_regex)
    five = four = three = two = one = ''
    if percentages and len(percentages) >= 5:
        five = percentages[0].strip()[:-1]
        four = percentages[1].strip()[:-1]
        three = percentages[2].strip()[:-1]
        two = percentages[3].strip()[:-1]
        one = percentages[4].strip()[:-1]
        print('percentages:' + five + ' ' + four + ' ' + three + ' ' + two + ' ' + one)
    else:
        five = four = three = two = one = '0'

    introduction_regex = '//span[@property="v:summary"]/text()'
    introduction = response.xpath(introduction_regex)
    if introduction and len(introduction):
        introduction = introduction[0].strip()
        print('introduction:' + introduction)
    else:
        introduction = ''

    same_likes_regex = '//dd/a/@href'
    same_likes = response.xpath(same_likes_regex)
    same_likes_li = []
    if same_likes and len(same_likes):
        print(same_likes)
        for like in same_likes:
            same_likes_li.append(get_movie_id(like))
        print(same_likes_li)

    pic_regex = '//img[@rel="v:image"]/@src'
    pic_url = response.xpath(pic_regex)
    if pic_url and len(pic_url):
        pic_url = pic_url[0].strip()
        print(pic_url)

    now_timestamp = time.time()     # 获取当前时间
    crawl_time = datetime.fromtimestamp(now_timestamp)   # 将时间戳（timestamp）转化为本地时间（datetime）
    crawl_time = str(crawl_time)
    print('crawl_time:' + crawl_time)

    info['did'] = did
    info['name'] = name
    info['year'] = year
    info['directors'] = directors
    info['writers'] = writers
    info['actors'] = actors
    info['types'] = types
    info['regions'] = regions
    info['languages'] = languages
    info['release_date'] = release_date
    info['runtime'] = runtime
    info['alias'] = alias
    info['imdb'] = imdb
    info['score'] = score
    info['num'] = num
    info['five'] = five
    info['four'] = four
    info['three'] = three
    info['two'] = two
    info['one'] = one
    info['introduction'] = introduction
    info['pic'] = pic_url
    info['crawl_time'] = crawl_time
    info['same_likes'] = same_likes_li

    return info


def get_response(url):
    time.sleep(random.random() * 3)

    headers = {"User-Agent": UserAgent().random}
    # 全局变量，公共代理
    global PUBLIC_PROXY

    while True:
        print('设置的proxy为：' + PUBLIC_PROXY)
        proxies = {
            'http': 'http://' + PUBLIC_PROXY,
            'https': 'https://' + PUBLIC_PROXY
        }
        try:
            response = requests.get(url, proxies=proxies, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            # 如果响应编码为200，说明请求成功，代理可用，则退出循环
            if response.status_code == 200:
                break
        except requests.exceptions.ConnectionError as e:
            print('Error', e.args)
        except Exception as e:
            print('Exception', e.args)
        # 如果代理不可用，则重新获取一个代理
        PUBLIC_PROXY = get_proxy()

    return response


def download_pic(info):
    if info['pic'] and len(info['pic']):
        response = get_response(info['pic'])
        folder = 'G:\\Graduation_Design\\mrs_storage\\movie\\'
        filename = info['did'] + '-' + str(uuid.uuid4())
        path = folder + filename + '.webp'
        with open(path, 'wb') as f:
            f.write(response.content)
        info['pic'] = filename + '.webp'
        print('图片下载完成:' + info['pic'])
    else:
        print('无可下载图片。')


def get_did_from_db(did):
    try:
        select_did_sql = "SELECT did FROM movie WHERE did = %s" % did
        cursor.execute(select_did_sql)  # 执行SQL语句
        res = cursor.fetchone()         # 获取执行结果
        return res
    except Exception as e:
        logging.error(e)


def save_info_into_db(info):
    try:
        keys = tuple(info.keys())
        values = tuple(info.values())
        # 这里因为same_likes不是movie这个表中的，所以剔除掉
        new_keys = ','.join(keys[:-1])
        new_values = ','.join(["%s"] * (len(keys) - 1))
        insert_info_sql = "insert into movie (%s) values (%s)" % (new_keys, new_values)
        cursor.execute(insert_info_sql, values[: -1])
        db.connection.commit()
    except Exception as e:
        logging.error(e)


def save_same_likes_into_db(info):
    try:
        did = info['did']
        same_likes = info['same_likes']
        for like in same_likes:
            sql = 'insert into same_likes (did, sid) values (%s)' % '%s, %s'
            cursor.execute(sql, (did, like))
        db.connection.commit()
    except Exception as e:
        logging.error(e)


def save_info(info):
    try:
        save_info_into_db(info)
        save_same_likes_into_db(info)
        print('数据已存入数据库中＜（＾－＾）＞')
    except Exception as e:
        logging.error(e)


def main():
    page_start = -20
    while True:
        page_start += 20
        print('page_start', str(page_start))
        # 获取电影详情的url列表
        movie_urls = get_movie_urls(page_start)
        print(movie_urls)
        print()

        for url in movie_urls:
            response = get_response(url)
            print('请求码为：', end=str(response.status_code))
            print()
            if response.status_code == 200:
                info = get_movie_info(response)
                # did表示豆瓣id，即电影的subject号码
                # 查询数据库中是否已经有did，如果不存在，则下载图片，并将数据存入数据库中
                isDidExists = get_did_from_db(info['did'])
                if isDidExists is None:
                    download_pic(info)  # 下载图片
                    save_info(info)     # 将info存入数据库中
                print(info)
                print()
            else:
                print('error')
                print()


if __name__ == '__main__':
    main()
