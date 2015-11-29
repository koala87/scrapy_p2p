#coding=utf-8

from scrapy.spiders import Spider
import scrapy
import os
import re
import json
import shutil
import logging

ROOT = os.path.dirname(os.path.abspath(__file__))

class Junrongdai(Spider):
    name = 'junrongdai'
    allowed_domains = ["junrongdai.com"]
    start_urls = ["http://www.junrongdai.com/invest/1_all_all_all_all_all_all"]

    num_project = 0
    dir_name = os.path.join(ROOT, name)
    first = True

    def parse(self, response):
        if Junrongdai.first:
            if os.path.exists(Junrongdai.dir_name):
                shutil.rmtree(Junrongdai.dir_name)
            os.makedirs(Junrongdai.dir_name)                        
            Junrongdai.first = False

        items = response.css('body > div > div > div.main > div.economicBox > div.economic')

        for item in items:
            title = item.css('h2.economicHead > div.economicTitle > a::text').extract()[0]
            link = 'http:' + item.css('h2.economicHead > div.economicTitle > a::attr(href)').extract()[0]
            pay_back_method = item.css('h2.economicHead > div.economicTitle01 > span::text').extract()[0]
            profit = item.css('div.economic_list > div.ecoBarLeft > div::text').extract()[0]
            time = item.css('div.economic_list > div.ecoBarRight > div::text').extract()[0]
            time_unit = item.css('div.economic_list > div.ecoBarRight > div > span::text').extract()[0]
            total = item.css('div:nth-child(3) > span > em::text').extract()[0]
            total_unit = item.css('div:nth-child(3) > span::text').extract()[1]
            lack_money = item.css('div:nth-child(4) > span > b::text').extract()[0]
            lack_money_unit = item.css('div:nth-child(4) > span::text').extract()[1]
            status =  item.css('a::text').extract()[0]
            company =  item.css('h2.economic_txt::text').extract()[0]

            # get obj id
            pos = link.rfind('/')
            obj_id = link[pos+1:]

            result = {
                'title' : title,
                'link' : link,
                'profit' : profit,
                'time' : time,
                'time_unit' : time_unit,
                'total' : total,
                'total_unit' : total_unit,
                'lack_money' : lack_money,
                'lack_money_unit' : lack_money_unit,
                'status' : status,
                'company' : company,
            }

            # write result
            fname = os.path.join(Junrongdai.dir_name, 'obj_%s_outline.txt' % obj_id)
            with open(fname, 'w') as fout:
                json.dump(result, fout, indent=4)
                # request detail page
                yield scrapy.Request(link, callback=self.parse_detail)            

            # request record
            # TODO: get record url
            #https://www.junrongdai.com/ProjectAction-getInvest.action?id=297ebc2d51142a5901511e8beda00143&skip=0&take=10&once=1448760716237
            #record_url = "http://www.xiaoniu88.com/product/detail/%s/invest/0/10" % prj_id
            #yield scrapy.Request(record_url, callback=self.parse_record)

        # request next page
        try:
            next_page = 'http:' + response.css('body > div > div > ul > li:nth-child(11) > a::attr(href)').extract()[0]
            if next_page:
                yield scrapy.Request(next_page, callback=self.parse) 
        except:
            pass


    def parse_detail(self, response):
        title = ''
        try:
            title = response.css('body > div.bgroundBox > div > div.column > div > div.columnLeftFirst > div.colTitle > h1::text').extract()[0]
        except:
            title = ''
        code = ''
        try:
            code = response.css('body > div.bgroundBox > div > div.column > div > div.columnLeftFirst > div.colTitle > span::text').extract()[0]
        except:
            code = ''
        total = response.css('body > div.bgroundBox > div > div.column > div > div.columnLeftSecond > div.colInnerLeft > span::text').extract()[0]
        total_unit = response.css('body > div.bgroundBox > div > div.column > div > div.columnLeftSecond > div.colInnerLeft > span > a::text').extract()[0]
        profit = response.css('body > div.bgroundBox > div > div.column > div > div.columnLeftSecond > div.colInnerMiddle > span::text').extract()[0]
        time = response.css('body > div.bgroundBox > div > div.column > div > div.columnLeftSecond > div.colInnerRight > span::text').extract()[0]
        time_unit = response.css('body > div.bgroundBox > div > div.column > div > div.columnLeftSecond > div.colInnerRight > span > a::text').extract()[0]
        progress = response.css('#target::text').extract()[0]
        start_time = response.css('body > div.bgroundBox > div > div.column > div > div.columnLeftFourth > div:nth-child(1) > p:nth-child(1)::text').extract()[0]
        pay_back_method = response.css('body > div.bgroundBox > div > div.column > div > div.columnLeftFourth > div:nth-child(1) > p:nth-child(2)::text').extract()[0]
        profit_method = response.css('body > div.bgroundBox > div > div.column > div > div.columnLeftFourth > div:nth-child(1) > p:nth-child(3)::text').extract()[0]
        end_time = response.css('body > div.bgroundBox > div > div.column > div > div.columnLeftFourth > div:nth-child(2) > p:nth-child(1)::text').extract()[0]
        safe_mode = response.css('body > div.bgroundBox > div > div.column > div > div.columnLeftFourth > div:nth-child(2) > p:nth-child(2) > a::text').extract()[0]
        safe_mode += response.css('body > div.bgroundBox > div > div.column > div > div.columnLeftFourth > div:nth-child(2) > p:nth-child(2)::text').extract()[1]
        tmp = response.css('body > div.bgroundBox > div > div.investBottomBox.clearFix > div.investBottomLeft > div.investInfo > div:nth-child(3) > div.investInfoContent01 > div > div::text').extract()
        borrower_outline = '##'.join([x.strip() for x in tmp])
        tmp = response.css('body > div.bgroundBox > div > div.investBottomBox.clearFix > div.investBottomLeft > div.investInfo > div:nth-child(3) > div:nth-child(3) > div.investInfoContentInner::text').extract()
        borrower_intro = '##'.join([x.strip() for x in tmp])
        borrower_purpose = ''
        try:
            borrower_purpose = response.css('body > div.bgroundBox > div > div.investBottomBox.clearFix > div.investBottomLeft > div.investInfo > div:nth-child(3) > div:nth-child(4) > div.investInfoContentInner::text').extract()[0].strip()
        except:
            borrower_purpose = ''
        tmp = response.css('body > div.bgroundBox > div > div.investBottomBox.clearFix > div.investBottomLeft > div.investInfo > div:nth-child(3) > div:nth-child(5) > div.investInfoContentInner::text').extract()
        pay_back_guarantee = '##'.join([x.strip() for x in tmp])
        safe_guarantee = ''
        try:
            safe_guarantee = response.css('body > div.bgroundBox > div > div.investBottomBox.clearFix > div.investBottomLeft > div.investInfo > div:nth-child(3) > div:nth-child(6) > div.investInfoContentInner::text').extract()[0].strip()
        except:
            safe_guarantee = ''
        law_case = response.css('body > div.bgroundBox > div > div.investBottomBox.clearFix > div.investBottomLeft > div.investInfo > div:nth-child(3) > div:nth-child(7) > div.investInfoContentInner::text').extract()
        trust_situation = response.css('body > div.bgroundBox > div > div.investBottomBox.clearFix > div.investBottomLeft > div.investInfo > div:nth-child(4) > div:nth-child(1) > div.investInfoContentInner::text').extract()[0]
        tmp = response.css('body > div.bgroundBox > div > div.investBottomBox.clearFix > div.investBottomLeft > div.investInfo > div:nth-child(4) > div:nth-child(2) > div.investInfoContentInner::text').extract()
        risk_safe = '##'.join([x.strip() for x in tmp])
        tmp = response.css('body > div.bgroundBox > div > div.investBottomBox.clearFix > div.investBottomLeft > div.investInfo > div:nth-child(4) > div:nth-child(2) > div.bx-wrapper > div.bx-viewport > div > li > a > img::attr(alt)').extract()
        card_names = '##'.join([x.strip() for x in tmp])
        tmp = response.css('body > div.bgroundBox > div > div.investBottomBox.clearFix > div.investBottomLeft > div.investInfo > div:nth-child(4) > div:nth-child(2) > div.bx-wrapper > div.bx-viewport > div > li > a > img::attr(src)').extract()
        card_srcs = '##'.join([x.strip() for x in tmp])

        result = {
            'title' : title,
            'code' : code,
            'total' : total,
            'total_unit' : total_unit,
            'profit' : profit,
            'profit_method' : profit_method,
            'time' : time,
            'time_unit' : time_unit,
            'progress' : progress,
            'start_time' : start_time,
            'end_time' : end_time,
            'safe_mode' : safe_mode,
            'borrower_outline' : borrower_outline,
            'borrower_intro' : borrower_intro,
            'borrower_purpose' : borrower_purpose,
            'pay_back_guarantee' : pay_back_guarantee,
            'safe_guarantee' : safe_guarantee,
            'law_case' : law_case,
            'trust_situation' : trust_situation,
            'risk_safe' : risk_safe,
            'card_names' : card_names,
            'card_srcs' : card_srcs,
        }
        # write result
        pos = response.url.rfind('/')
        obj_id = response.url[pos+1:]
        fname = os.path.join(Junrongdai.dir_name, 'obj_%s_detail.txt' % obj_id)
        with open(fname, 'w') as fout:
            json.dump(result, fout, indent=4)


    def parse_record(self, response):
        pat = re.search('.*detail/(\d+)/invest/(\d+)/10', response.url)
        if pat:
            # write record json into file
            prj_id, page_num = pat.groups()
            fname = os.path.join(Junrongdai.dir_name, 'obj_%s_record_page_%s.txt' % (prj_id, page_num))
            body = json.loads(response.body)
            if not body['data']:
                return
            with open(fname, 'w') as fout:
                json.dump(body, fout, indent=4)

            # request next record page
            next_page = int(page_num) + 1
            next_url = re.sub('invest/(\d+)/10', 'invest/%s/10' % next_page, response.url)
            yield scrapy.Request(next_url, callback=self.parse_record)
