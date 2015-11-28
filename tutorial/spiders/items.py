# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class P2PItem(scrapy.Item):
    title = Field()
    href = Field()
    icon = Field()
    level = Field()
    question = Field()
    area = Field()
    money = Field()
    time = Field()
    profit = Field()
    detail = Field()
    supplier_name = Field()
    company = Field()
    desc = Field()
