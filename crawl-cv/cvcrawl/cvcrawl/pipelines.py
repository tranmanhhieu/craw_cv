# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient
import datetime as dt
from .settings import *
class CvcrawlPipeline:

    def __init__(self):

        if MONGODB_USERNAME != '' and MONGODB_HOST != '127.0.0.1':
            self.mongo_uri = MongoClient(
                "mongodb://" + MONGODB_USERNAME + ":" + MONGODB_PASSWORD + "@" + MONGODB_HOST + ":" + str(MONGODB_PORT))
        else:
            self.mongo_uri = MongoClient(
                'mongodb://' + MONGODB_HOST + ':' + MONGODB_PORT)
        self.mongo_db = DATABASE

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection

        self.db = self.mongo_uri[self.mongo_db]

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.mongo_uri.close()

    def process_item(self, item, spider):
        self.db[spider.name].insert_one(dict(item))
        return item
