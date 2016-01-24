# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LCBOItem(Item):
    name = Field()
    prod_type = Field()
    prod_code = Field()
    price = Field()
    volume = Field()
    pass
