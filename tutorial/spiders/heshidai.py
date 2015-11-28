#coding=utf-8

from scrapy.spiders import Spider
from items import P2PItem
import re

class P2P(Spider):
    name = 'heshidai'
    allowed_domains = ["ppmoney.com"]
    start_urls = ["https://www.heshidai.com/lctz/index.html"]

    def parse(self, response):
        item = response.xpath('//*[@id="financialDIV"]/ul[2]/li[1]/a')
        print item.extract()
