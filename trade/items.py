# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TradeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DataDailyfutureItem(scrapy.Item):
    date = scrapy.Field()
    commodity = scrapy.Field()
    contract = scrapy.Field()
    open = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    close = scrapy.Field()
    volume = scrapy.Field()
    adjustment = scrapy.Field()
    oi = scrapy.Field()
    session = scrapy.Field()
