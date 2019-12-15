# -*- coding: utf-8 -*-
import scrapy
import datetime
from trade.items import ThreepsDailyoptionItem
from urllib.parse import urlencode
import calendar

class ThreepsDailyoptionSpider(scrapy.Spider):
    name = 'threeps_dailyoption'
    allowed_domains = ['http://www.taifex.com.tw']

    def start_requests(self):

        def get_period(year, month):
            """
            Get first and last day of specified year and month
            """
            first_weekday, days = calendar.monthrange(year, month)
            first = datetime.date(year=year, month=month, day=1)
            last = datetime.date(year=year, month=month, day=days)
            return first, last
        nowdate = datetime.date.today() + datetime.timedelta(days = -1)
        start, end = map(lambda d: d.strftime('%Y/%m/%d'),
                         get_period(year=2019,
                                    month=12))
        commodity_list = ['TXO']
        for commodity in commodity_list:
            params = {
                "queryStartDate": start,
                "queryEndDate": nowdate.strftime('%Y/%m/%d'),
                "commodityId": commodity}
            url = "http://www.taifex.com.tw/cht/3/dlCallsAndPutsDateDown?" + \
                urlencode(params)
            print(url)
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse)


    def parse(self, response):
        df = response.text.replace('"',"").split("\n")
        item = ThreepsDailyoptionItem()
        for i in range(int((len(df)-2)/6)):
            date = datetime.datetime.strptime(df[6*i+1].split(",")[0], '%Y/%m/%d').date()
            item['date'] = str(date)
            item['commodity'] = "TXO"
            item['call_wz'] = int(int(df[6*i+3].split(",")[15]))
            item['put_wz'] = int(int(df[6*i+6].split(",")[15]))
            item['call_zy'] = int(int(df[6*i+1].split(",")[15]))
            item['put_zy'] = int(int(df[6*i+4].split(",")[15]))
            yield item
