#coding=utf-8

from scrapy.spiders import Spider
import scrapy
import os
import re
import json
import shutil
import logging

ROOT = os.path.dirname(os.path.abspath(__file__))

class Ppmoney(Spider):
    name = 'ppmoney'
    allowed_domains = ["ppmoney.com"]
    start_urls = ["http://www.ppmoney.com/project/PrjListJson/-1/1/All"]

    num_project = 0
    dir_name = os.path.join(ROOT, name)
    first = True

    def parse(self, response):
        pat = re.search('.*/(\d+)/All', response.url)
        
        if pat:
            page_num = int(pat.groups()[0])
            
            body = json.loads(response.body)
            project_list = body['PackageList']['Data']
            if len(project_list) == 0:
                return

            for project in project_list:
                link = project['link']
                project_id = project['prjId']
                if Ppmoney.first:
                    if os.path.exists(Ppmoney.dir_name):
                        shutil.rmtree(Ppmoney.dir_name)
                    os.makedirs(Ppmoney.dir_name)                        
                    Ppmoney.first = False

                fname = os.path.join(Ppmoney.dir_name, 'obj_%d_outline.txt' % project_id)
                with open(fname, 'w') as fout:
                    json.dump(project, fout, indent=4)

                # request detail
                detail_url = 'http://www.ppmoney.com/' + link
                yield scrapy.Request(detail_url, callback=self.parse_detail)            

            next_page = page_num + 1
            next_url = re.sub('(\d+)/All', '%d/All' % next_page, response.url)
            yield scrapy.Request(next_url, callback=self.parse) 

    def parse_detail(self, response):
        title = response.xpath('//*[@id="prjTitle"]/h3/@title').extract()[0]
        time = response.xpath('/html/body/div[4]/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[3]/div[2]/p/span/text()').extract()[0]
        time_unit = response.xpath('/html/body/div[4]/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[3]/div[2]/p/text()').extract()[1].strip()
        total = response.xpath('/html/body/div[4]/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/div[2]/p/span/text()').extract()[0]
        total_unit = response.xpath('/html/body/div[4]/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/div[2]/p/text()').extract()[0]
        profit_method = response.xpath('/html/body/div[4]/div[2]/div[1]/div[1]/div[2]/div/div[2]/ul/li[1]/span/text()').extract()[0]
        pay_back_method = response.xpath('/html/body/div[4]/div[2]/div[1]/div[1]/div[2]/div/div[2]/ul/li[3]/span/text()').extract()[0].strip()
        begin_time = response.xpath('/html/body/div[4]/div[2]/div[1]/div[1]/div[2]/div/div[2]/ul/li[2]/span/text()').extract()[0]
        end_time = ''
        try:
            end_time = response.xpath('/html/body/div[4]/div[2]/div[1]/div[1]/div[2]/div/div[2]/ul/li[5]/text()').extract()[0]
        except:
            end_time = ''
        pay_back_time = response.xpath('/html/body/div[4]/div[2]/div[1]/div[1]/div[2]/div/div[2]/ul/li[4]/span/text()').extract()[0]
        note = response.xpath('/html/body/div[4]/div[2]/div[1]/div[1]/div[2]/div/div[3]/span[2]/text()').extract()[0]
        intro = ','.join(response.xpath('//*[@id="intro"]/div/p').extract())
        guarantee = ','.join(response.xpath('/html/body/div[4]/div[2]/div[1]/div[3]/div/div/div[2]/ul/li/div').extract())
        
        result = {
            'title' : title,
            'time' : time,
            'time_uint' : time_unit,
            'total' : total,
            'total_unit' : total_unit,
            'profit_method' : profit_method,
            'pay_back_method' : pay_back_method,
            'begin_time' : begin_time,
            'end_time' : end_time,
            'pay_back_time' : pay_back_time,
            'note' : note,
            'intro' : intro,
            'guarantee' : guarantee,
        }
        pos = response.url.rfind('/')
        prj_id = response.url[pos+1:]
        fname = os.path.join(Ppmoney.dir_name, 'obj_%s_detail.txt' % prj_id)
        with open(fname, 'w') as fout:
            json.dump(result, fout, indent=4)

        status_url = 'https://www.ppmoney.com/project/AsyncLoadPrjStatus/%s' % prj_id
        yield  scrapy.Request(status_url, self.parse_status)

        record_url = 'https://www.ppmoney.com/investment/records/%s_1_6' % prj_id
        yield  scrapy.Request(record_url, self.parse_record)


    def parse_status(self, response):
        pos = response.url.rfind('/')
        prj_id = response.url[pos+1:]
        fname = os.path.join(Ppmoney.dir_name, 'obj_%s_status.txt' % prj_id)
        status = json.loads(response.body)
        with open(fname, 'w') as fout:
            json.dump(status, fout, indent=4)


    def parse_record(self, response):
        pos = response.url.rfind('/')
        record = response.url[pos+1:]
        parts = record.split('_')
        prj_id, page = parts[0:2]

        fname = os.path.join(Ppmoney.dir_name, 'obj_%s_record_page_%s.txt' % (prj_id, page))
        record = json.loads(response.body)
        
        if not record['Data']['Rows']:
            return

        with open(fname, 'a') as fout:
            json.dump(record, fout, indent=4)

        next_page = int(page) + 1

        next_url = re.sub('records/(.*)', 'records/%s_%d_6' % (prj_id, next_page), response.url)
        yield  scrapy.Request(next_url, self.parse_record)
