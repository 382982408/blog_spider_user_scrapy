# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

class BlogspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class json_with_encoding_pipeline(object):
    def __init__(self):
        #codecs比open功能强大，可以很方便的处理文件编码问题
        self.file = codecs.open('article.json','w', encoding='utf-8')
    def process_item(self, item, spider):
        #ensure_ascii设置很重要，item可以很方便转dict
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item
    def spider_closed(self):
        '''
        spider_closed是爬虫关闭的信号量，当爬虫完毕时，自动调用
        '''
        self.file.close()