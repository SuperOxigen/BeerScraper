# -*- coding: utf-8 -*-

from scrapy.spiders     import Spider
from scrapy.selector    import Selector
from BeerScraper        import items
from scrapy.http        import Request

from re import compile
from urlparse import urlparse


def url_concate(url, path):
    url_data = urlparse(url)
    return "%s://%s%s" % (url_data.scheme, url_data.netloc, path)

class LCBOSpider(Spider):
    name = "lcbo-crawler"
    allowed_domains = ["www.lcbo.com",]
    start_urls = ["http://www.lcbo.com/",]



    def parse(self, response):
        sel = Selector(response)
        submenus = sel.xpath('//*[@id="mainmenu"]//li[@class="dropdown-submenu"]/a[contains(@href,"/lcbo/catalog/")]').extract()

        link_pattern = compile(r'href="(?P<link>.+)".*\>(?P<title>.+)\<')

        for submenu in submenus:
            if link_pattern.search(submenu):
                data = link_pattern.search(submenu).groupdict()          
                url = url_concate(response.url, data['link'])

                yield Request(url, callback=self.catalog_parse)

    def catalog_parse(self, response):
        sel = Selector(response)

        products = sel.xpath('//*[contains(@class, "products")]//div[contains(@class, "product")]').extract()

        for product in products:
            yield self.catalog_entry_parse(product)

    def catalog_entry_parse(self, body):
        sel = Selector(text=body)

        titles = sel.xpath('//*[contains(@class, "product-name")]/a/text()').extract()
        prices = sel.xpath('//*[contains(@class, "product-price")]//*[@class="price"]/text()').extract()
        codes  = sel.xpath('//*[contains(@class, "product-name")]//*[contains(@class, "product-code")]').extract()
        volume = sel.xpath('//*[contains(@class, "product-name")]//*[contains(@class, "product-code")]//*[contains(@class, "plp-volume-grid")]/text()').extract()

        code_pattern = compile(r'LCBO\D+(?P<code>\d+)')
        volume_pattern = compile(r'(?P<volume>\d+)\s(?P<units>(?:m[lL])|(?:[lL]))')

        if len(titles) == 1 and len(prices) == 1:
            item = items.BeerScraperItem()
            item['name'] = titles[0].strip()
            item['price'] = prices[0]
            if code_pattern.search(codes[0]):
                item['prod_code'] = code_pattern.search(codes[0]).groupdict()['code']
            else:
                item['prod_code'] = 'NA'
            if len(volume) == 1 and volume_pattern.search(volume[0]):
                vdict = volume_pattern.search(volume[0]).groupdict()
                item['volume'] = "%s %s" % (vdict['volume'], vdict['units'])
            return item
        else:
            # print("No good %d %d %d" % (len(titles), len(prices), len(codes)))
            return None

