# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

from taobao.settings import *


class TaobaoPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE, charset=DB_CHARSET)
        self.cursor = self.conn.cursor()
        self.data = []

    def close_spider(self, spider):
        """
                关闭爬虫，回调
                :param spider:
                :return:
        """
        # self.conn.commit()
        if len(self.data) > 0:
            self.insertMany()
        self.conn.close()

    def open_spider(self, spider):
        """
        打开爬虫，回调
        :param spider:
        :return:
        """
        pass

    def process_item(self, item, spider):
        """
        爬取到数据，回调（多次）
        :param item:
        :param spider:
        :return:
        """
        title = item.get('title', "")
        prize = item.get('prize', "")
        content = item.get('content', "")
        people_buy = item.get('people_buy', 0)
        shop_name = item.get('shop_name', "")
        shop_url = item.get('shop_url', "")
        item_type = item.get('item_type', "")

        self.data.append((title, prize, content, people_buy, shop_name, shop_url, item_type))
        if len(self.data) == 100:
            self.insertMany()
        return item

    def insertMany(self):
        # print('insert into `taobao` VALUES (%s, %s, %s, %s, %s, %s)', self.data)
        self.cursor.executemany('insert into `taobao` VALUES (%s, %s, %s, %s, %s, %s, %s)', self.data)
        self.conn.commit()
        self.data.clear()
