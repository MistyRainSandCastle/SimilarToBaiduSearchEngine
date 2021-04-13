from scrapy import signals
from scrapy.exceptions import NotConfigured


class RedisSpiderClosedEx(object):

    def __init__(self, idleNumber, crawler):
        self.crawler = crawler
        self.idleNumber = idleNumber
        self.idleCount = 0

    @classmethod
    def from_crawler(cls, crawler):

        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        idleNumber = crawler.settings.getint('IDLE_NUMBER', 360)

        extens = cls(idleNumber, crawler)

        crawler.signals.connect(extens.spider_opened, signal=signals.spider_opened)

        crawler.signals.connect(extens.spider_closed, signal=signals.spider_closed)

        crawler.signals.connect(extens.spider_idle, signal=signals.spider_idle)

        return extens

    def spider_opened(self, spider):
        spider.logger.info("opened spider {}, Allow waiting time:{} second".format(spider.name, self.idleNumber * 5))

    def spider_closed(self, spider):
        spider.logger.info(
            "closed spider {}, Waiting time exceeded {} second".format(spider.name, self.idleNumber * 5))

    def spider_idle(self, spider):


        if spider.server.exists(spider.redis_key) or spider.server.exists(spider.redis_request):
            self.idleCount = 0
        else:
            self.idleCount += 1

        if self.idleCount > self.idleNumber:
            self.crawler.engine.close_spider(spider, 'Waiting time exceeded')
