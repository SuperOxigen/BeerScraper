# -*- coding: utf-8 -*-

from scrapy.spiders     import Spider
from scrapy.selector    import Selector
from BeerScraper        import items
from scrapy.http        import Request

from re import compile
from urlparse import urlparse, parse_qs, urlsplit, urlunsplit
from urllib import urlencode
# from html import unescape
from HTMLParser import HTMLParser

unescape = HTMLParser().unescape

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
            item = items.LCBOItem()
            item['name'] = titles[0].strip()
            item['price'] = prices[0]
            item['retailer'] = "LCBO"
            if code_pattern.search(codes[0]):
                item['prod_code'] = code_pattern.search(codes[0]).groupdict()['code']
            else:
                item['prod_code'] = 'NA'
            if len(volume) == 1 and volume_pattern.search(volume[0]):
                item['volume'] = volume_pattern.search(volume[0]).groupdict()
            return item
        else:
            # print("No good %d %d %d" % (len(titles), len(prices), len(codes)))
            return None

class SAQCrawler(Spider):
    name = "saq-crawler"
    allowed_domains = ["www.saq.com",]
    start_urls = ["https://www.saq.com/content/SAQ/en/produits.html",]

    def parse(self, response):
        sel = Selector(response)

        catagories = sel.xpath('//ul[@class="gridProducts"]/li/a').extract()

        link_pattern = compile(r'href="(?P<link>.+)".*\>(?P<title>.+)\<')        

        for catagory in catagories:
            if link_pattern.search(catagory):
                link_data = link_pattern.search(catagory).groupdict()
                url = url_concate(response.url, unescape(link_data['link'])) # + "pageSize=100"
                yield Request(url, self.catalog_parse)

    def catalog_parse(self, response):
        qdict = parse_qs(urlparse(response.url).query)
        if "pageSize" in qdict.keys() and "1000" not in qdict["pageSize"]:
            scheme, netloc, path, _, fragment = urlsplit(response.url)
            qdict["pageSize"] = ["1000"]
            qs = urlencode(qdict, doseq=True)
            url = urlunsplit((scheme, netloc, path, qs, fragment))
            yield Request(url, self.catalog_parse)
        else:
            sel = Selector(response)

            rows = sel.xpath('//*[@id="resultatRecherche"]//div[contains(@id, "result")]').extract()

            # total_pages('//div[@class="PagerResultatLinks"]')

            for row in rows:
                yield self.catalog_entry_parse(row)



    def catalog_entry_parse(self, body):
        sel = Selector(text = body)

        names = sel.xpath('//p[@class="nom"]/a/text()').extract()
        details = sel.xpath('//p[@class="desc"]').extract()
        prices = sel.xpath('//td[@class="price"]/a/text()').extract()

        detail_pattern = compile(r'\>(?P<type_data>[\S\s]+)\<br\>(?P<volume_raw>[\S\s]+)\<br\>[\S\s]+\D(?P<code>\d+)[\S\s]+\<')
        volume_pattern = compile(r'\D(?P<volume>\d+)\D(?P<units>(?:m[lL])|(?:[lL]))')

        if len(names) == 1 and len(details) == 1 and len(prices) == 1:
            item = items.SAQItem()
            item['name'] = names[0]
            item['price'] = prices[0]
            item['retailer'] = "SAQ"
            details[0] = unescape(details[0])
            if detail_pattern.search(details[0]):
                ddict = detail_pattern.search(details[0]).groupdict()
                item['prod_code'] = ddict['code']
                item['prod_type'] = ddict['type_data'].strip()
                volume = unescape(ddict['volume_raw']).strip()
                if volume_pattern.search(volume):
                    item['volume'] = volume_pattern.search(volume).groupdict()
            else:
                item['prod_code'] = details[0]
            return item
        else:
            return None


class BeerStoreCrawler(Spider):
    name = "saq-crawler"
    allowed_domains = ["www.thebeerstore.ca",]
    start_urls = ["http://www.thebeerstore.ca/beers",]    

    def parse(self, response):
        sel = Selector(response)

        catagories = sel.xpath()        
        pass
