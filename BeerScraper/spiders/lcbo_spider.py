from scrapy.spiders import Spider
from scrapy.selector import Selector

from tutorial.items import lcboItem


class lcboSpider(Spider):
    name = "lcbo"
    allowed_domains = ["www.lcbo.com/"]
    start_urls = [
        "http://www.lcbo.com/lcbo/catalog/red-wine/11025",
    ]

    def parse(self, response):
        sel = Selector(response)
        sel.xpath('//div[@class="product-name"]')
        items = []

        for site in sites:
            item = Website()
            item['name'] = site.xpath('a/text()').extract()
            item['url'] = site.xpath('a/@href').extract()
            item['description'] = site.xpath('text()').re('-\s[^\n]*\\r')
            items.append(item)

        return items