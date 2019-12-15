# -*- coding: utf-8 -*-
import scrapy
import datetime
from trade.items import ThreepsDailyfutureItem
from urllib.parse import urlencode
import calendar

class ThreepsDailyFutureSpider(scrapy.Spider):
    name = 'threeps_dailyfuture'
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
        commodity_list = ['MXF', 'TXF']
        for commodity in commodity_list:
            params = {
                "goday": "",
                "queryStartDate": start,
                "queryEndDate": nowdate.strftime('%Y/%m/%d'),
                "commodityId": commodity}
            url = "http://www.taifex.com.tw/cht/3/dlFutContractsDateDown?" + \
                urlencode(params)
            print(url)
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse)


    def parse(self, response):
        df = response.text.replace('"',"").replace("'","").split("\r\n")
        item = ThreepsDailyfutureItem()
        for i in range(int((len(df)-2)/3)):
            date = datetime.datetime.strptime(df[3*i+1].split(",")[0], '%Y/%m/%d').date()
            item['date'] = str(date)
            item['commodity'] = df[3*i+1].split(",")[1].replace(
                "小型臺指期貨","MTX").replace("臺股期貨","TX")
            item['zy_amount'] = int(round(float(df[3*i+1].split(",")[13]),4))
            item['tz_amount'] = int(round(float(df[3*i+2].split(",")[13]),4))
            item['wz_amount'] = int(round(float(df[3*i+3].split(",")[13]),4))
            item['sum_amount'] = int(round((item['zy_amount'] + item['tz_amount'] + item['wz_amount']),4))
            yield item

