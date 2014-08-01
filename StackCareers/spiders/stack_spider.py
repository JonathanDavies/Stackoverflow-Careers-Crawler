import scrapy

from StackCareers.items import Job

class StackSpider(scrapy.Spider):
    name = "stack"
    allowed_domains = ["careers.stackoverflow.com"]
    start_urls = [
        "http://careers.stackoverflow.com/uk/jobs?searchTerm=&location=london",
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@data-jobid]'):
            item = Job()
            item['title'] = sel.xpath('h3/a/text()').extract()
            item['company'] = [x.strip() for x in sel.xpath('p/span[@class="employer"]/text()').extract()]
            #item['company'] = map(str.strip, sel.xpath('p/span[@class="employer"]/text()').extract())
            yield item