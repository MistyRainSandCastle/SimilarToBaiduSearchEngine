from scrapy import signals
from scrapy.exceptions import NotConfigured

class RecordProNumEx(object):
    def __init__(self,fileName):
        self.fileName = fileName

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured
        extens = cls(crawler.settings.get('CONFIG_READ_SETTING'))
        crawler.signals.connect(extens.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(extens.spider_closed, signal=signals.spider_closed)
        return extens


    def WriteFile(self, typeStr):
        with open(self.fileName, 'w') as f:
            f.write("SPIDER:{0}".format(typeStr))

    def spider_opened(self, spider):
        self.WriteFile("OPENED")
        spider.logger.info("opened spider {}, Writing setting file:{}".format(spider.name, "OPENED"))

    def spider_closed(self, spider):
        self.WriteFile("CLOSED")
        spider.logger.info("closed spider {}, Writing setting file:{}".format(spider.name, "CLOSED"))
