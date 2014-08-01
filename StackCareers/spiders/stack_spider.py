import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from StackCareers.items import Job

class StackSpider(CrawlSpider):
    name = "stack"
    allowed_domains = ["careers.stackoverflow.com"]
    start_urls = [
        "http://careers.stackoverflow.com/uk/jobs?searchTerm=&location=london",
    ]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="pagination"]/a[text()="next"]')), callback='parse_start_url', follow=True),
    )

    def parse_start_url(self, response):
        for sel in response.xpath('//div[@data-jobid]'):
            item = Job()
            item['title'] = sel.xpath('h3/a/text()').extract()
            item['company'] = [x.strip() for x in sel.xpath('p/span[@class="employer"]/text()').extract()]
            #item['company'] = map(str.strip, sel.xpath('p/span[@class="employer"]/text()').extract())
            yield item