import json
import os
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from StackCareers.items import Company

DOMAIN = 'careers.stackoverflow.com'

def get_companies():
    companies = set()
    if os.path.isfile('companies.json'):
        with open('companies.json') as f:
            try:
                data = json.load(f)
                companies.update(line['name'].strip() for line in data)
            except Exception:
                pass
    return companies


class StackSpider(CrawlSpider):
    companies = get_companies()

    name = "companies"
    allowed_domains = [DOMAIN]
    start_urls = [
        "http://careers.stackoverflow.com/uk/jobs/companies/location/london",
    ]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="pagination"]/a[text()="next"]')), callback='parse_start_url', follow=True),
    )

    def parse_start_url(self, response):
        for sel in response.xpath('//div[@class="list companies"]/div'):
            item = Company()
            item['name']    = ''.join(sel.xpath('a/text()').extract()).strip()
            item['link']    = DOMAIN + ''.join(sel.xpath('a/@href').extract()).strip()
            if item['name'] not in self.companies:
                self.companies.add(item['name'])
                yield item