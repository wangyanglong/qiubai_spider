# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiubaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    _id = scrapy.Field()
    _type = scrapy.Field()
    _author = scrapy.Field()
    _avatar = scrapy.Field()
    _url = scrapy.Field()
    _content = scrapy.Field()
    _micon = scrapy.Field()
    _wicon = scrapy.Field()
    _like = scrapy.Field()
    _status = scrapy.Field()
    # comment = scrapy.Field()
