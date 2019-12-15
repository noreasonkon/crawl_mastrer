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

class ThreepsDailyfutureItem(scrapy.Item):
    date = scrapy.Field()
    commodity = scrapy.Field()
    zy_amount = scrapy.Field()
    tz_amount = scrapy.Field()
    wz_amount = scrapy.Field()
    sum_amount = scrapy.Field()

class ThreepsDailyoptionItem(scrapy.Item):
    date = scrapy.Field()
    commodity = scrapy.Field()
    call_wz = scrapy.Field()
    put_wz = scrapy.Field()
    call_zy = scrapy.Field()
    put_zy = scrapy.Field()


class DataDailyoptionItem(scrapy.Item):
    date = scrapy.Field()
    commodity = scrapy.Field()
    contract = scrapy.Field()
    strike = scrapy.Field()
    pc = scrapy.Field()
    open = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    close = scrapy.Field()
    volume = scrapy.Field()
    adjustment = scrapy.Field()
    oi = scrapy.Field()
    session = scrapy.Field()

class BigpsDailyfutureItem(scrapy.Item):
    date = scrapy.Field()
    commodity = scrapy.Field()
    commodity_cn = scrapy.Field()
    contract = scrapy.Field()
    kind = scrapy.Field()
    buy_5 = scrapy.Field()
    sell_5 = scrapy.Field()
    buy_10 = scrapy.Field()
    sell_10 = scrapy.Field()
    oi = scrapy.Field()


class BigpsDailyoptionItem(scrapy.Item):
    date = scrapy.Field()
    commodity = scrapy.Field()
    commodity_cn = scrapy.Field()
    pc = scrapy.Field()
    contract = scrapy.Field()
    kind = scrapy.Field()
    buy_5 = scrapy.Field()
    sell_5 = scrapy.Field()
    buy_10 = scrapy.Field()
    sell_10 = scrapy.Field()
    oi = scrapy.Field()

