# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import pymongo
import const
import MySQLdb
import datetime

insert_sql ="INSERT INTO `wp_spider`(`_update`,"\
"`_create`,`_qid`,`_author`,`_type`,`_url`,`_content`,`_pic`,`_like`,`_status`)"\
"VALUES(%r,%r,'%s',%r,'%s','%s','%s',%r,%d,%d)"
    
update_sql = "UPDATE wp_spider SET `_update`=%r,"\
"`_like`=%d WHERE `_qid`='%s'"


class QiubaiPipeline(object):
    def __init__(self):
        conn = MySQLdb.connect(host=const.mysql_url,
                                user=const.mysql_user,
                                passwd = const.mysql_passwd,
                                db=const.mysql_db,
                                charset='utf8')
        self.conn = conn
        self.cursor = conn.cursor()

    def process_item(self, item, spider):
        cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if item['_qid'] and item['_status']:
            self.cursor.execute("SELECT _author FROM wp_spider WHERE _qid=%s",(item["_qid"],))
            result = self.cursor.fetchone()
            if not result:#insert
                author = item['_author']
                if author:
                    author = author.encode('utf-8')
                else:
                    author = "null"
                pic = item['_pic']
                if pic:
                    pic = pic.encode('utf-8')
                else:
                    pic = "null"
                like = item['_like']
                if like:
                    like = int(like)
                else:
                    like = 0
                sql = insert_sql%(cur_time,cur_time,item['_qid'].encode('utf-8'),
                    author,item['_type'].encode('utf-8'),item['_url'].encode('utf-8'),
                    item['_content'],pic,like,int(item['_status']))
                print "sql",sql
                print "end"
                self.cursor.execute(sql)
            else:
                like = item['_like']
                if like:
                    like = int(like)
                else:
                    like = 0
                sql = update_sql%(cur_time,like,item['_qid'].encode('utf-8'))
                self.cursor.execute(sql)
            self.conn.commit()
        else:
            raise DropItem("invalid item struct:%r",item)
        return item
