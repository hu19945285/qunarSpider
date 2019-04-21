# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class QunarsitePipeline(object):
    def process_item(self, item, spider):
        return item

class MySQLPipeline:
    def open_spider(self,spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy_default')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', 'root')
        self.db_conn = MySQLdb.connect(host=host, port=port, db=db,user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()
    
    def close_spider(self,spider):
        self.db_conn.commit()
        self.db_conn.close()
    
    def process_item(self, item, spider):
        if spider.name=='citySpider':        
            self.insert_city_db(item)
        elif spider.name=='siteSpider':
            self.insert_site_db(item)
        return item
    
    def insert_city_db(self,item):
        values=(
                item['city_name'],
                item['province_name'],
                item['city_httpsite'],
                item['city_id'],
                )
        sql = 'INSERT INTO city VALUES (%s,%s,%s,%s)'
        self.db_cur.execute(sql, values)
        
    def insert_site_db(self,item):
        values=(
                item['spot_id'],
                item['spot_name'],
                item['spot_cityId'],
                item['spot_rank'],
                item['spot_intro'],
                item['spot_playTime'],
                item['spot_grade'],
                item['spot_addr'],
                item['spot_tel'],
                item['spot_openTime'],
                item['spot_ticket'],
                item['spot_visitSeason'],
                item['spot_trafficGuide'],
                item['spot_commentsNum'],
                item['spot_5starNum'],
                item['spot_4starNum'],
                item['spot_3starNum'],
                item['spot_2starNum'],
                item['spot_1starNum'],            
                )
        sql = 'INSERT INTO site VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.db_cur.execute(sql, values)        