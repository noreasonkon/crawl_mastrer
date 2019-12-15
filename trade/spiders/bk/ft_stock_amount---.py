# -*- coding: utf-8 -*-
import scrapy
import datetime
import calendar
import pandas as pd
from io import StringIO
from urllib.parse import urlencode
from trade.items import FtStockAmountItem
import json
import requests

class FtStockAmountSpider(scrapy.Spider):
    name = 'ft_stock_amount'
    allowed_domains = ['www.twse.com']

    def __init__(self):
        self.run_date = datetime.date.today()
        self.start_date = self.run_date
        self.end_date = self.start_date + datetime.timedelta(days=-31)

    def start_requests(self):
        params = {
            "response": "json",
            "date": '20191211',
            "type": 'MS',
            "_": '1495581694979'
            }

        url = "http://www.twse.com.tw/exchangeReport/MI_INDEX"# + \
           # urlencode(params)
        print(url)
        print("---------------")


        #print(scrapy.Request(url=url, dont_filter=True).text)

        #yield requests.get(url)
       # yield scrapy.Request(
     #       url=url,
     #       dont_filter=True
     #       header = headers)
        yield scrapy.http.JsonRequest(url, data=params)


    def transform_data(self, response):
        data_list = json.loads(response.text)
        df = pd.DataFrame(data_list['data8']).T
        print(df)
        columns = df.loc[0].tolist()
        df = df.drop([0], axis=0)
        df.columns = columns
        return df

    def parse(self, response):
        print("------------22---")
        df = self.transform_data(response)

        item = FtStockAmountItem()
        item['date'] = df["交易日期"]
        item['up_amount'] = df['上漲(漲停)'][2].split("(")[0]
        item['top_amount'] = df['上漲(漲停)'][2].split("(")[1].split(")")[0]
        item['down_amount'] = df['下跌(跌停)'][2].split("(")[0]
        item['bot_amount'] = df['下跌(跌停)'][2].split("(")[1].split(")")[0]
        item['stop_amount1'] = df['持平'][1]
        item['stop_amount2'] = df['持平'][2]
        yield item
