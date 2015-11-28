#coding=utf-8

from scrapy.spiders import Spider
import scrapy
import os
import re
import json
import shutil
import logging

ROOT = os.path.dirname(os.path.abspath(__file__))

class Xiaoniu(Spider):
    name = 'xiaoniu'
    allowed_domains = ["xiaoniu88.com"]
    start_urls = ["http://www.xiaoniu88.com/product/planning"]

    num_project = 0
    dir_name = os.path.join(ROOT, name)
    first = True

    def parse(self, response):
        if Xiaoniu.first:
            if os.path.exists(Xiaoniu.dir_name):
                shutil.rmtree(Xiaoniu.dir_name)
            os.makedirs(Xiaoniu.dir_name)                        
            Xiaoniu.first = False

        items = response.css('body > div.mail > div.g-o > div.center > div.right > div.list-area > div.list-box > ul')
        for item in items:
            title = item.css('li.sig-l > h1 > span > a::attr(title)').extract()[0]
            link = item.css('li.sig-l > h1 > span > a::attr(href)').extract()[0]
            profit = item.css('li.sig-l > span:nth-child(2) > em::text').extract()[0]
            time = item.css('li.sig-l > span:nth-child(3) > em::text').extract()[0] 
            time_unit = item.css('li.sig-l > span:nth-child(3)::text').extract()[0].strip()
            total = item.css('li.sig-l > span:nth-child(4) > em::text').extract()[0]
            total_unit = item.css('li.sig-l > span:nth-child(4)::text').extract()[0]
            begin_time = item.css('li.sig-l > span:nth-child(5) > em::text').extract()[0]
            people_num = item.css('li.sig-l > span:nth-child(6) > em::text').extract()[0]
            start_money = item.css('li.sig-l > span:nth-child(7) > em::text').extract()[0]

            pos = link.rfind('/')
            prj_id = link[pos+1:]

            result = {
                'title' : title,
                'link' : link,
                'profit' : profit,
                'time' : time,
                'time_unit' : time_unit,
                'total' : total,
                'total_unit' : total_unit,
                'begin_time' : begin_time,
                'people_num' : people_num,
                'start_money' : start_money,
            }

            # write result
            fname = os.path.join(Xiaoniu.dir_name, 'obj_%s_outline.txt' % prj_id)
            with open(fname, 'w') as fout:
                json.dump(result, fout, indent=4)
                # request detail page
                detail_url = 'http://www.xiaoniu88.com' + link
                yield scrapy.Request(detail_url, callback=self.parse_detail)            

            # request record
            record_url = "http://www.xiaoniu88.com/product/detail/%s/invest/0/10" % prj_id
            yield scrapy.Request(record_url, callback=self.parse_record)

        # request next page
        next_page = response.css('body > div.mail > div.g-o > div.center > div.right > div.list-area > div.pages > div > a:nth-child(10)::attr(href)').extract()
        if next_page:
            next_url = "http://www.xiaoniu88.com" + next_page[0]
            yield scrapy.Request(next_url, callback=self.parse) 


    def parse_detail(self, response):
        
        if response.url.find('login') != -1:
            return
        title = response.css('body > div.mail > div.g-o > div.center.detail-bg > div.detail-til > h1::text').extract()[0]
        total = response.css('body > div.mail > div.g-o > div.center.detail-bg > div.detail-con > div.dtl-l > ul.pro-info01.pro-zq > li.l > span.un::text').extract()[0]
        profit = response.css('body > div.mail > div.g-o > div.center.detail-bg > div.detail-con > div.dtl-l > ul.pro-info01.pro-zq > li.c > span.un > span::text').extract()[0].strip().replace('\t', '').replace(' ','').replace('\r\n', '')
        time = response.css('body > div.mail > div.g-o > div.center.detail-bg > div.detail-con > div.dtl-l > ul.pro-info01.pro-zq > li.r > span.un::text').extract()[0].strip()
        time_unit = response.css('body > div.mail > div.g-o > div.center.detail-bg > div.detail-con > div.dtl-l > ul.pro-info01.pro-zq > li.r > span.un > i::text').extract()[0]
        pay_back_method = response.css('body > div.mail > div.g-o > div.center.detail-bg > div.detail-con > div.dtl-l > ul.pro-info02.axn-zs > li:nth-child(1) > span.lay-f::text').extract()[0]
        safe_mode = response.css('body > div.mail > div.g-o > div.center.detail-bg > div.detail-con > div.dtl-l > ul.pro-info02.axn-zs > li:nth-child(2)::text').extract()[0]
        create_time = response.css('body > div.mail > div.g-o > div.center.detail-bg > div.detail-con > div.dtl-l > ul.pro-info02.axn-zs > li:nth-child(3)::text').extract()[0]
        progress = response.css('body > div.mail > div.g-o > div.center.detail-bg > div.detail-con > div.dtl-l > ul.pro-info02.axn-zs > li:nth-child(4) > span:nth-child(3)::text').extract()[0]
        publish_time = response.css('body > div.mail > div.g-o > div.center.detail-bg > div.detail-con > div.dtl-l > ul.pro-info02.axn-zs > li:nth-child(5)::text').extract()[1].strip()
        people_num = response.css('body > div.mail > div.g-o > div.center.detail-bg > div.detail-con > div.dtl-l > ul.pro-info02.axn-zs > li:nth-child(6)::text').extract()[0]
        intro = response.css('body > div.mail > div.g-o > div.center.detl-bottom > div.detl-l > div > p::text').extract()[0]        
        left_money = ''
        left_money_unit = ''
        start_money = ''
        try:
            left_money = response.css('#form > div > ul > li:nth-child(1) > span.do-r > strong::text').extract()[0]
        except:
            left_money = ''
        try:
            left_money_unit = response.css('#form > div > ul > li:nth-child(1)::text').extract()[0]
        except:
            left_moeny_unit = ''
        try:
            start_money = response.css('#form > div > ul > li.hig.tomonery > span.do-r::text').extract()[0]
        except:
            start_money = ''
        
        result = {
            'title' : title,
            'total' : total,
            'profit' : profit,
            'time' : time,
            'time_unit' : time_unit,
            'pay_back_method' : pay_back_method,
            'safe_mode' : safe_mode,
            'create_time' : create_time,
            'progress' : progress,
            'publish_time' : publish_time,
            'people_num' : people_num,
            'intro' : intro,
            'left_money' : left_money,
            'left_money_unit' : left_money_unit,
            'start_money' : start_money,
        }
        # write result
        pos = response.url.rfind('/')
        prj_id = response.url[pos+1:]
        fname = os.path.join(Xiaoniu.dir_name, 'obj_%s_detail.txt' % prj_id)
        with open(fname, 'w') as fout:
            json.dump(result, fout, indent=4)


    def parse_record(self, response):
        pat = re.search('.*detail/(\d+)/invest/(\d+)/10', response.url)
        if pat:
            # write record json into file
            prj_id, page_num = pat.groups()
            fname = os.path.join(Xiaoniu.dir_name, 'obj_%s_record_page_%s.txt' % (prj_id, page_num))
            body = json.loads(response.body)
            if not body['data']:
                return
            with open(fname, 'w') as fout:
                json.dump(body, fout, indent=4)

            # request next record page
            next_page = int(page_num) + 1
            next_url = re.sub('invest/(\d+)/10', 'invest/%s/10' % next_page, response.url)
            yield scrapy.Request(next_url, callback=self.parse_record)
