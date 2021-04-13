# -*- coding: utf-8 -*-
from SearchSpider.Modules.CommonModule import  WEBPAGETYPE
from SearchSpider.items import SearchSpiderItem, SearchItemLoader
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from SearchSpider.Modules.ExtractContentInfo import ExtractInfo


class HfutspiderSpider(RedisCrawlSpider):
    name = 'HfutSpider'
    allowed_domains = ['hfut.edu.cn']
    redis_key = 'HfutSpider:start_urls'
    redis_request = 'HfutSpider:requests'
    rules = (
        Rule(LinkExtractor(allow=r''), callback='ParseItem', follow=True),
    )

    def ParseItem(self, response):
        if response.meta["pageType"] == WEBPAGETYPE['INDEXPAGE'] or \
                response.meta["pageType"] == WEBPAGETYPE['CONTENTPAGE']:
            isIndex=response.meta["pageType"] == WEBPAGETYPE['INDEXPAGE']
            itemLoader = SearchItemLoader(item=SearchSpiderItem(), response=response)
            extract = ExtractInfo()
            extract.ExtactProcess(response.text,isIndex)
            itemLoader.add_value("url", response.url)
            itemLoader.add_value("urlOrigin", response.url)
            if response.meta["pageType"]== WEBPAGETYPE['CONTENTPAGE']:
                itemLoader.add_css("imageUrl", "img::attr(src)")
            itemLoader.add_value("title", extract.GetTitle())
            itemLoader.add_value("content", extract.GetContent())
            itemLoader.add_value("createdDate", extract.GetDate())
            itemLoader.add_value("isIndex", isIndex)
            return itemLoader.load_item()
