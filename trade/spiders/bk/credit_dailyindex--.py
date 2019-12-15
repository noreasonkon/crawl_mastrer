# -*- coding: utf-8 -*-
import scrapy
import datetime
import calendar
import pandas as pd
from io import StringIO
from urllib.parse import urlencode
from trade.items import DataDailyoptionItem


class CreditDailyindexSpider(scrapy.Spider):
    name = 'credit_dailyindex'
    allowed_domains = ['www.tse.com']

    def __init__(self):
        self.run_date = datetime.date.today()
        self.start_date = self.run_date
        self.end_date = self.start_date + datetime.timedelta(days=-31)

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
                         get_period(year=self.run_date.year,
                                    month=self.run_date.month))
        params = {
            "response": "json",
            "date": "20191211",
            "selectType": 'MS'}

        start, end = map(lambda d: d.strftime('%Y/%m/%d'),
                         get_period(year=self.run_date.year,
                                          month=self.run_date.month))

        url = "http://www.tse.com.tw/exchangeReport/MI_MARGN?" + \
            urlencode(params)
        yield scrapy.Request(
            url=url,
            callback=self.parse)

    def transform_data(self, response):
        df = pd.read_csv(
            StringIO("\n".join([i.translate({ord(c): None for c in ' '})
                                for i in response.text.split('\n')
                                if len(i.split(',')) >= 10])), index_col=False)
        df = df.loc[(df["成交量"] > 0) | (df["未沖銷契約數"] != "-") | (df["結算價"] != "-")]
        df["交易日期"] = df["交易日期"].str.replace("/", "-")
        df["到期月份(週別)"] = df["到期月份(週別)"].astype(str).str.replace(" ", "")
        df["契約"] = df["契約"].str.replace(" ", "")
        df["交易時段"] = df["交易時段"].str.replace("一般", "AM").str.replace("盤後", "PM")
        df["買賣權"] = df["買賣權"].str.replace("買權","Call").str.replace("賣權","Put").str.replace(" ","")
        df = df.dropna(subset=['交易日期'])   

        return df

    def parse(self, response):
        print("--------------")
        def fmt_float(value):
            try:
                return float(value)
            except Exception:
                return 0.0
        df = self.transform_data(response)
        item = DataDailyoptionItem()
        for idx in df.index:
            item['date'] = df["交易日期"][idx]
            item['commodity'] = df["契約"][idx]
            item['contract'] = df["到期月份(週別)"][idx]
            item['strike'] = df["履約價"][idx]
            item['pc'] = df["買賣權"][idx]
            item['open'] = fmt_float(df["開盤價"][idx])
            item['high'] = fmt_float(df["最高價"][idx])
            item['low'] = fmt_float(df["最低價"][idx])
            item['close'] = fmt_float(df["收盤價"][idx])
            item['volume'] = fmt_float(df["成交量"][idx])
            item['adjustment'] = fmt_float(df["結算價"][idx])
            item['oi'] = fmt_float(df["未沖銷契約數"][idx])
            item['session'] = df["交易時段"][idx]
            yield item
