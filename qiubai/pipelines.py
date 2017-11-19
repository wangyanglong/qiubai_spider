# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import pymongo
import const
import MySQLdb
import datetime

#pip install mysqlclient

"""
CREATE TABLE IF NOT EXISTS `wp_spider`(
    `ID` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
    `_update` datetime DEFAULT NULL COMMENT '更新时间',
    `_create` datetime NOT NULL COMMENT '创建时间',
    `_qid` varchar(80) NOT NULL unique COMMENT '文章ID',
    `_author` varchar(80) DEFAULT NULL COMMENT '作者ID',
    `_type` varchar(120) NOT NULL COMMENT '文章类型',
    `_url`  varchar(80) NOT NULL COMMENT '文章链接',
    `_content` blob NOT NULL COMMENT '正文',
    `_pic`  varchar(500) DEFAULT NULL COMMENT '配图',
    `_like` bigint(20) DEFAULT 0 COMMENT '原始喜欢数',
    `_status` tinyint DEFAULT 0 COMMENT '爬虫状态',
    PRIMARY KEY ( `ID` ),
    KEY `_create` (`_create`),
    KEY `_update` (`_update`),
    KEY `_like` (`_like`),
    KEY `_status` (`_status`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

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
