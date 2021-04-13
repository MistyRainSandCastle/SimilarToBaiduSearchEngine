from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

from scrapy_redis import get_redis_from_settings
from scrapy_redis.pipelines import default_serialize
from . import defaults


class RedisNotDownloadUrl(BaseDupeFilter):
    def __init__(self, server,
                 key=defaults.NOT_DOWNLOAD_URL_KEY,
                 serialize_func=default_serialize):
        self.server = server
        self.key = key
        self.serialize_func = serialize_func

    def request_seen(self, request):
        fp = request_fingerprint(request)
        added = self.server.sadd(self.key, fp)
        return added == 0

    def is_exist(self, request):
        fp = request_fingerprint(request)
        return self.server.sismember(self.key, fp)

    @classmethod
    def from_spider(cls, spider):
        settings = spider.settings
        server = get_redis_from_settings(settings)
        not_download_key = settings.get("SCHEDULER_NOT_DOWNLOAD_KEY", defaults.SCHEDULER_NOT_DOWNLOAD_KEY)
        key = not_download_key % {'spider': spider.name}
        return cls(server, key=key)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    @classmethod
    def from_settings(cls, settings):
        server = get_redis_from_settings(settings)
        key = '%s:notdownloadurl' % settings.get("SPIDER_NAME", "HfutSpider")
        return cls(server, key=key)
