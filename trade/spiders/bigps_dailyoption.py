# -*- coding: utf-8 -*-
import scrapy
import datetime
import calendar
import pandas as pd
from io import StringIO
from urllib.parse import urlencode
from trade.items import BigpsDailyoptionItem


class BigpsDailyoptionSpider(scrapy.Spider):
    name = 'bigps_dailyoption'
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
        start, end = map(lambda d: d.strftime('%Y/%m/%d'),
                         get_period(year=2019,
                                    month=12))
        params = {
            "queryStartDate": start,
            "queryEndDate": end}
        url = "http://www.taifex.com.tw/cht/3/dlLargeTraderOptDown?" + \
            urlencode(params)
        yield scrapy.Request(
            url=url,
            callback=self.parse)

    def transform_data(self, response):
        df = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '})
                                            for i in response.text.split('\n') 
                                            if len(i.split(',')) >= 10 ])), header=0)
        
        df.columns = ['date','commodity', 'commodity_cn', 'pc', 'contract', 
                      'kind','buy_5','sell_5' ,'buy_10', 'sell_10','oi']
        df = df.dropna(subset=['date'])     
        df['date'] = df['date'].str.replace("/","-")
        for Column in df.columns:
            df[Column] = df[Column].astype(str)   
        df.pc = df.pc.replace("賣權","Put").replace("買權","Call")      
        df = df.loc[(df.contract != "-") & (df.commodity == 'TXO')]


        return df

    def parse(self, response):
        df = self.transform_data(response)
        item = BigpsDailyoptionItem()
        for idx in df.index:
            item['date'] = df["date"][idx]
            item['commodity'] = df["commodity"][idx]
            item['commodity_cn'] = df["commodity_cn"][idx]
            item['pc'] = (df["pc"][idx])
            item['contract'] = (df["contract"][idx])
            item['kind'] = (df["kind"][idx])
            item['buy_5'] = (df["buy_5"][idx])
            item['sell_5'] = (df["sell_5"][idx])
            item['buy_10'] = (df["buy_10"][idx])
            item['sell_10'] = (df["sell_10"][idx])
            item['oi'] = (df["oi"][idx])
            yield item

