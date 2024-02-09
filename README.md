# 电影推荐系统（爬虫）

## 前言

总项目名称：`电影推荐系统`

项目采用`前后端分离`：

1. 前端：
   - 仓库地址：[movie_recommendation_system_vue](https://github.com/jun-wei-zeng/movie_recommendation_system_vue)
   - 技术栈：`Vue3` + `Element Plus` + `axios`等
2. 后端：
   - 仓库地址：[movie_recommendation_system_server](https://github.com/jun-wei-zeng/movie_recommendation_system_server)
   - 技术栈：`Spring Boot` + `Spring Security` + `Redis` + `MyBatis-Plus`等
3. 数据爬虫：
   - 简介：爬取项目所需的电影基本信息数据和用户评价数据等并存储。
   - 仓库地址：[douban_movie_spider_mrs](https://github.com/jun-wei-zeng/douban_movie_spider_mrs/tree/master)
   - 技术栈：`requests` + `lxml`

系统功能模块总览：

![系统功能模块.png](README_IMG/系统功能模块.png)

# douban_movie_spider_mrs

电影推荐系统（爬虫：requests+lxml）

目录文件说明：

- `mrs.sql`用于构建所有项目所需数据库表。

- 爬虫代码在`./spiders`文件夹中: 

  - `movie_info_spider.py`: 电影详情信息爬虫
  - `movie_comments_spider.py`: 电影评价信息爬虫
