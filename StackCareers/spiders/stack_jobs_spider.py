import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from StackCareers.items import Job

class StackSpider(CrawlSpider):
    name = "jobs"
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
            item['title']   = ''.join(sel.xpath('h3/a/text()').extract())
            item['company'] = ''.join(sel.xpath('p/span[@class="employer"]/text()').extract()).strip()
            item['tags']    = sel.xpath('p[@class="tags"]/a/text()').extract()
            yield item