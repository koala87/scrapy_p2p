#coding=utf-8

import scrapy
from scrapy.spiders import Spider
import re

class Yitongdai(Spider):
    name = 'yitongdai'
    allowed_domains = ['app.etongdai.com']
    start_urls = ["http://app.etongdai.com/investments/index"]

    def parse(self, response):
        items = response.xpath('//div[@class="xiangmu"]/dl/dt/h3/a/@href').extract()

        for url in items:
            yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        left = response.xpath('//div[@class="xiangmu left"]')
        right = response.xpath('//div[@class="right tz_info "]')
        detail = response.xpath('//div[@class="detail_con con24"]')

        title = left.xpath('.//h3/text()').extract()
        profit = left.xpath('.//div[@class="shuju"]/ul/li/i/text()').extract()
        money = left.xpath('.//div[@class="shuju"]/ul/li/span/text()').extract()
        
        ratio = left.xpath('.//p[@class="bar"]/em/text()').extract()
        level = left.xpath('.//div[@class="chart ab_r"]/div[@class="xy_tu"]/span/text()').extract()

        pay_back = left.xpath('.//div[@class="xshuju"]/dl[@class="tzs1 dl_h"]/dd')
        pay_method = pay_back[0].xpath('.//span/text()').extract()
        pay_time = pay_back[1].xpath('.//span/text()').extract()
        pay_left = pay_back[2].xpath('.//span/text()').extract()
        pay_type = pay_back[3].xpath('.//span/text()').extract()

        total = right.xpath('.//p/span/text()').extract()

        #basic = detail.xpath('.//div[@class="tab_c"]/p/span/text()').extract()
        basic = detail.xpath('.//div[@class="tab_c"]/span/text()').extract()
        if not basic:
            basic = detail.xpath('.//div[@class="tab_c"]/p/span').extract()

        record_header = detail.xpath('.//div[@class="det_c2 tab_c"]/table/thead/tr/td/text()').extract()
        record_body = detail.xpath('.//div[@class="det_c2 tab_c"]/table/tbody').extract()

        material_header = detail.xpath('.//div[@class="tab_c"]/table/thead/tr/td/text()').extract()
        material_body = detail.xpath('.//div[@class="tab_c"]/table').extract()

        way = detail.xpath('.//div[@class="det_c4 tab_c"]').extract()

        table = response.xpath('//*[@id="item_info"]').extract()
        #print title, profit, money
        #print pay_method, pay_time, pay_left, pay_type
        #print ratio, level
        #print response.url
        #print total
        print response.url
        #print basic
        #print record_header
        #print record_body
        #print material_header
        #print material_body
        #print way
        print table
