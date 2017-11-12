# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import const

class QiubaiPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            const.mongo_url,
            const.mongo_port
        )
        db = connection[const.mongo_db]
        self.col = db[const.mongo_col]
        self.col.ensure_index("_qid",unique=True)

    def process_item(self, item, spider):
        if item['_qid'] and item['_status']:
            self.col.update({'_qid':item['_qid']},dict(item),True)
            return item
        else:
            raise DropItem("invalid item struct:%r",item)
        return item
