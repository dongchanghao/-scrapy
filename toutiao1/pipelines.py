# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors

class MySQLPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host = 'localhost',
            port = 3306,
            db = 'toutiao',
            user = 'root',
            passwd = '1333',#密码
            charset = 'utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()
    def process_item(self, item, spider):
        #sql = "insert into information(id,classify_id,title,source_url,source,abstract,label,comments_count,behot_time,nowtime,duration,middle_image)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s',%s,%s)"
        sql = "insert into information(id,classify_id,title,source_url,source,abstract,label,comments_count,behot_time,nowtime,duration,middle_image)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #params = (item['id'],item['classify_id'],pymysql.escape_string(item['title']),pymysql.escape_string(item['source_url']),pymysql.escape_string(item['source']),pymysql.escape_string(item['abstract']),pymysql.escape_string(item['label']),item['comments_count'],pymysql.escape_string(item['behot_time']),pymysql.escape_string(item['nowtime'].replace('/','')),item['duration'],pymysql.escape_string(item['middle_image']))
        params = (item['id'],item['classify_id'],pymysql.escape_string(item['title']),pymysql.escape_string(item['source_url']),pymysql.escape_string(item['source']),pymysql.escape_string(item['abstract']),pymysql.escape_string(item['label']),item['comments_count'],pymysql.escape_string(item['behot_time']),pymysql.escape_string(item['nowtime']),item['duration'],pymysql.escape_string(item['middle_image']))
        print(sql)
        # for i in params:
        #     print(i,':',type(i))
        # print('params',params)
        self.cursor.execute(sql, params)
        self.connect.commit()
        return item