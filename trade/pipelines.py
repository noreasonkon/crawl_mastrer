# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import logging


class TradePipeline(object):
    def process_item(self, item, spider):
        return item


class DataDailyFuturePipeline(object):
    def __init__(self, sqlite_file, sqlite_table):
        self.sqlite_file = sqlite_file
        self.sqlite_table = sqlite_table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_file=crawler.settings.get(
                'SQLITE_DB_NAME'),
            sqlite_table='data_dailyfuture'
        )

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.sqlite_file)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        insert_sql = "insert or replace into {0}({1}) values ({2})".format(
            self.sqlite_table, ', '.join(item.keys()),
            ', '.join(['?'] * len(item.keys())))
        values = tuple(item.values())

        #print(insert_sql)
        #print(values)
        try:
            self.cur.execute(insert_sql, values)
            self.conn.commit()
        except sqlite3.Error:
            print("fail")
        #    logging.msg("Item stored : " % item, level=logging.DEBUG)
        return item
