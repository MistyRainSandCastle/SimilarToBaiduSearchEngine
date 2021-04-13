import redis

# For standalone use.
DUPEFILTER_KEY = 'dupefilter:%(timestamp)s'

PIPELINE_KEY = '%(spider)s:items'

NOT_VISIT_URL_KEY = '%(spider)s:notvisiturl'
NOT_DOWNLOAD_URL_KEY = '%(spider)s:notdownloadurl'

REDIS_CLS = redis.StrictRedis
REDIS_ENCODING = 'utf-8'
# Sane connection defaults.
REDIS_PARAMS = {
    'socket_timeout': 30,
    'socket_connect_timeout': 30,
    'retry_on_timeout': True,
    'encoding': REDIS_ENCODING,
}

SCHEDULER_QUEUE_KEY = '%(spider)s:requests'
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'
SCHEDULER_DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
SCHEDULER_NOT_VISIT_KEY = NOT_VISIT_URL_KEY
SCHEDULER_NOT_VISIT_CLASS = 'scrapy_redis.notvisit.RedisNotVisitUrl'
SCHEDULER_NOT_DOWNLOAD_KEY = NOT_DOWNLOAD_URL_KEY
SCHEDULER_NOT_DOWNLOAD_CLASS = 'scrapy_redis.notdownload.RedisNotDownloadUrl'

START_URLS_KEY = '%(name)s:start_urls'
START_URLS_AS_SET = False
