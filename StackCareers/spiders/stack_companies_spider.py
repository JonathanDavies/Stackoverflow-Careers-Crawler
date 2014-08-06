import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from StackCareers.items import Company

DOMAIN = 'careers.stackoverflow.com'

class StackSpider(CrawlSpider):
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
            item['name']    = ''.join(sel.xpath('a/text()').extract())
            item['link']    = DOMAIN + ''.join(sel.xpath('a/@href').extract())
            yield item