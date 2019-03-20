# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ToutiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 新闻标题
    id = scrapy.Field()
    classify_id = scrapy.Field()
    title=scrapy.Field()
    #作者
    source = scrapy.Field()
    # 新闻链接
    source_url=scrapy.Field()
    # 新闻摘要
    abstract=scrapy.Field()
    # 新闻标签
    label=scrapy.Field()
    # 新闻分类
    #news_class=scrapy.Field()
    #评论数
    comments_count = scrapy.Field()
    behot_time = scrapy.Field()
    nowtime = scrapy.Field()
    duration = scrapy.Field()
    middle_image = scrapy.Field()
