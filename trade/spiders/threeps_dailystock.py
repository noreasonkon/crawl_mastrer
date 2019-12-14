# -*- coding: utf-8 -*-
import scrapy


class ThreepsDailystockSpider(scrapy.Spider):
    name = 'threeps_dailystock'
    allowed_domains = ['http://www.taifex.com.tw/cht/3/dlFutContractsDateDown']
    custon_settings = {'ITEM_PIPELINES': {
        'trade.pipelines.DataDailyFuturePipeline': 300}}


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
            "goday": "",
            "queryStartDate": start,
            "queryEndDate": end,
            "commodityId": 'MXF'}

        url = "http://www.taifex.com.tw/cht/3/dlFutContractsDateDown?" + \
            urlencode(params)
        yield scrapy.Request(
            url=url,
            callback=self.parse)

    def transform_data(self, response):
        df = pd.read_csv(
            StringIO("\n".join([i.translate({ord(c): None for c in ' '})
                                for i in response.text.split('\n')
                                if len(i.split(',')) >= 10])), index_col=False)
        df = df.loc[df["成交量"] > 0]
        df.loc[:,"交易日期"] = df["交易日期"].str.replace("/", "-")
        df.loc[:,"到期月份(週別)"] = df["到期月份(週別)"].astype(str).str.replace(" ", "")
        df.loc[:,"契約"] = df["契約"].str.replace(" ", "")
        df.loc[:,"交易時段"] = df["交易時段"].str.replace("一般", "AM"
                                            ).replace("盤後", "PM")
        df = df.dropna(subset=['收盤價'])                            
        return df

    def parse(self, response):
        Tx_array = res.text.replace('"',"").replace("'","").split("\r\n")
        try:
            index_array = range(int((len(Tx_array)-2)/3))
            Date0 = Tx_array[1].split(",")[0]
            Date = datetime.date(int(Date0.split("/")[0]), int(Date0.split("/")[1]), int(Date0.split("/")[2]))
        except:
            print  (Date0 + "   Fail")

        for i in index_array:
            ins = 'insert into threeps_dailyfuture(DATE ,commodity, ZY_amount,TZ_amount,WZ_amount,sum_amount) VALUES(?,?,?,?,?,?)'
            Date0 = Tx_array[3*i+1].split(",")[0]
            Date = datetime.date(int(Date0.split("/")[0]), int(Date0.split("/")[1]), int(Date0.split("/")[2]))
            commodity = "MTX"
            Future_ZY = int(round(int(Tx_array[3*i+1].split(",")[13]),4))
            Future_TZ = int(round(int(Tx_array[3*i+2].split(",")[13]),4))
            Future_WZ = int(round(int(Tx_array[3*i+3].split(",")[13]),4))
            Future_Sum = int(round((Future_ZY + Future_TZ + Future_WZ),4))
            INSERTDATA = (str(Date),commodity,float(Future_ZY),float(Future_TZ),float(Future_WZ),float(Future_Sum))
            try:
                curs.execute(ins,INSERTDATA) 

            except:
                print  (str(Date) + " Data Repeat")
            conn.commit()
    #print  (Date0 + "   Sucess")
    return 
        df = self.transform_data(df)
        item = DataDailyfutureItem()
        for idx in df.index:
            item['date'] = df["交易日期"][idx]
            item['commodity'] = df["契約"][idx]
            item['contract'] = df["到期月份(週別)"][idx]
            item['open'] = fmt_float(df["開盤價"][idx])
            item['high'] = fmt_float(df["最高價"][idx])
            item['low'] = fmt_float(df["最低價"][idx])
            item['close'] = fmt_float(df["收盤價"][idx])
            item['volume'] = fmt_float(df["成交量"][idx])
            item['adjustment'] = fmt_float(df["結算價"][idx])
            item['oi'] = fmt_float(df["未沖銷契約數"][idx])
            item['session'] = df["交易時段"][idx]
            yield item
