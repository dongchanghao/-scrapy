# -*- coding: utf-8 -*-
import scrapy
import json
from toutiao1.items import ToutiaoItem
import hashlib
import execjs
import time
import random
import re
import html

from scrapy.http import Request

class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    allowed_domains = ['www.toutiao.com']
    max_behot_time = 0
    category = '__all__'
    start_urls = ['https://www.toutiao.com/api/pc/feed/?category={}&utm_source=toutiao&widen=1&max_behot_time=0'.format(category)]
    classify = {'__all__':1,'news_hot':2,'news_tech':3,'news_entertainment':4,'news_game':5,'news_sport':6,'news_car':7,'news_finance':8,'news_military':9,'news_world':10,'news_fashion':11,
                'news_travel':12,'news_discovery':13,'news_baby':14,'news_regimen':15,'news_essay':16,'news_history':17,'news_food':18,'news_politics_general':19,'news_society':20,
                'selected':21,'news_health':22,'science_all':23,'news_politics':24,'news_media':25,'news_nature':26,'news_agriculture':27,
                'news_traditional_culture':28,'news_edu':29,'news_culture':30,'news_ohotography':31,'news_house':32,'digital':33,'emotion':34}
    def start_requests(self):
        headers = {'Accept': '*/*',
                   'Accept-Language': 'zh-CN',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
                   'Connection': 'Keep-Alive',
                   'referer': 'https://www.toutiao.com/ch/news_hot/',
                             }
        for i in range(0,30000):
            Honey = json.loads(self.get_js())
            eas = Honey['as']
            ecp = Honey['cp']
            signature = Honey['_signature']
            url = 'https://www.toutiao.com/api/pc/feed/?category={}&utm_source=toutiao&widen=1&max_behot_time={}&max_behot_time_tmp={}&tadrequire=true&as={}&cp={}&_signature={}'.format(
                self.category, self.max_behot_time, self.max_behot_time, eas, ecp, signature)
            time.sleep(random.random()*2+2)
            #print(url)
            yield Request(url,callback=self.parse,dont_filter=True,headers=headers)
    def parse(self, response):
        result = json.loads(response.text)
        print(result)
        if 'data' in result:
            length = len(result['data'])
            for k in range(0, length):
                item = ToutiaoItem()
                now = time.time()
                if 'tag' in result['data'][k]:
                    if not result['message'] != 'error' or result['data'][k]['tag'] != 'ad':
                        item['id'] = int(result['data'][k]['item_id'])
                        item['title'] = result['data'][k]['title']
                        item['source'] = result['data'][k]['source']
                        #item['tag'] = result['data'][k]['tag']
                        item['source_url'] = 'https://www.toutiao.com/a' + result['data'][k]['source_url'][7:]
                        if result['data'][k]['tag'] in self.classify.keys():
                            item['classify_id'] = self.classify[result['data'][k]['tag']]
                        else:
                            item['classify_id'] = 35
                        try:
                            item['comments_count'] = result['data'][k]['comments_count']
                        except:
                            item['comments_count'] = ''
                        try:
                            item['label'] = ','.join(result['data'][k]['label'])
                        except:
                            item['label'] = ''
                        try:
                            item['middle_image'] = result['data'][k]['middle_image']
                        except:
                            item['middle_image'] = ''
                        try:
                            item['abstract'] = result['data'][k]['abstract']
                        except:
                            item['abstract'] = ''
                        behot = int(result['data'][k]['behot_time'])
                        item['behot_time'] = time.strftime('"%Y-%m-%d %H:%M:%S"', time.localtime(behot))
                        item['nowtime'] = time.strftime('"%Y-%m-%d %H:%M:%S"', time.localtime(now))
                        item['duration'] = (now - behot)
                        yield item

    def getHoney(self, t):  #####根据JS脚本破解as ,cp
        # t = int(time.time())  #获取当前时间
        # t=1534389637
        # print(t)
        e = str('%X' % t)  ##格式化时间
        # print(e)
        m1 = hashlib.md5()  ##MD5加密
        m1.update(str(t).encode(encoding='utf-8'))  ##转化格式
        i = str(m1.hexdigest()).upper()  ####转化大写
        # print(i)
        n = i[0:5]  ##获取前5位
        a = i[-5:]  ##获取后5位
        s = ''
        r = ''
        for x in range(0, 5):
            s += n[x] + e[x]
            r += e[x + 3] + a[x]
        eas = 'A1' + s + e[-3:]
        ecp = e[0:3] + r + 'E1'
        # print(eas)
        # print(ecp)
        return eas, ecp

    def get_js(self):

        f = open(r"D:\python练习\toutiao\toutiao-TAC.sign.js", 'r', encoding='UTF-8')#js位置
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
        ctx = execjs.compile(htmlstr)
        return ctx.call('get_as_cp_signature')

