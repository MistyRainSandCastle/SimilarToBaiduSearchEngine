# -*- coding: utf-8 -*-
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, MapCompose
from SearchSpider.Modules.CommonModule import ConstValue
import re
import scrapy


class SearchItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def getDomain(value):
    res = re.match(ConstValue['RE_SORT_MATCH'], value)
    return "" if res is None else res.group(1)


class SearchSpiderItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    isIndex=scrapy.Field()
    imageResult=scrapy.Field()
    urlOrigin = scrapy.Field(
        input_processor=MapCompose(getDomain)
    )
    createdDate = scrapy.Field()
    imageUrl = scrapy.Field(
        output_processor=Join(",")
    )
