# -*- coding: utf-8 -*-

import scrapy


class Job(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    tags = scrapy.Field()


class Company(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()