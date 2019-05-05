import scrapy
from scrapy import Selector
from cnblogSpider.items import CnblogspiderItem

class CnBlogsSpider(scrapy.Spider):
    name = "cnblogs"
    allowed_domains = ["cnblogs.com"]
    start_urls = ["http://www.cnblogs.com/qiyeboy/"]

    def parse(self, response):
        papers = response.xpath(".//*[@class='day']")
        for paper in papers:
            url = paper.xpath(".//*[@class='postTitle']/a/@href").extract()
            title = paper.xpath(".//*[@class='postTitle']/a/text()").extract()
            time = paper.xpath(".//*[@class='dayTitle']/a/text()").extract()
            content = paper.xpath(".//*[@class='postTitle']/a/text()").extract()[0]

            item = CnblogspiderItem(url=url, title=title, time=time, content=content)
            yield item # make parse method as generator

            next_page = Selector(response).re(u'<a href="(\S*)">下一页</a>')
            if next_page:
                yield scrapy.Request(url=next_page[0], callback=self.parse)

