# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .mysql_config import create_aws_connection


class Movielens1MPipeline:
    def process_item(self, item, spider):
        return item

from scrapy.exporters import CsvItemExporter
# movielens1m.pipelines.CsvPipeline
class CsvPipeline:
    def __init__(self):
        self.file = open('posts.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

import pymysql   
class SavingToMySQLPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.connection = create_aws_connection()
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        #we need to return the item below as Scrapy expects us to!
        return item

    def store_db(self, item):
        #添加记录
        self.cursor.execute(""" INSERT INTO imdb_movies (name, url, time, genre, release_time, intro, directors, writers,starts, completed)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s); """, (
            item["name"],
            item["url"],
            item["time"],item["genre"],item["release_time"],item["intro"],item["directors"],item["writers"],item["starts"],'1'
        ))
        self.connection.commit()
        #更新links表
        sql = "UPDATE imdb_movies_links SET spider_completed=1 WHERE url=%s"

        # 执行更新
        data = [(item["url"])]
        self.cursor.executemany(sql, data)
        self.connection.commit()