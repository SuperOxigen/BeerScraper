# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from BeerScraper import items

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


# //div[@class="product-name"
# click "glyphicon glyphicon-play next" to go to the next pg


# @Names of drinks
# scrapy shell http://www.lcbo.com/lcbo/catalog/red-wine/11025
# response.xpath("//div[@class='product-name']/a/@title").extract()

# @Prices
# response.xpath("//div[@class='price-wrapper']/div[@class='price']/text()").extract()

# @Product Code
# response.xpath("//small[@class='product-code']/text()").extract()

# @volume - needs to get rid of | (soldas, x in # per bought)
# response.xpath("//span[@class='plp-volume plp-volume-list']/text()").extract()

