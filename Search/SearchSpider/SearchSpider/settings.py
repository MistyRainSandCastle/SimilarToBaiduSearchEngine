# -*- coding: utf-8 -*-

# Scrapy settings for SearchSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = 'SearchSpider'

SPIDER_MODULES = ['SearchSpider.spiders']
NEWSPIDER_MODULE = 'SearchSpider.spiders'

# os.path.insert(os.path.abspath(os.path.dirname(__file__)))
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'SearchSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# DOWNLOAD_TIMEOUT = 50
LOG_LEVEL = 'INFO'
LOG_FILE = 'exception.log'
COOKIES_ENABLED = False
RETRY_ENABLED = False
# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'SearchSpider.middlewares.SearchspiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#
DOWNLOADER_MIDDLEWARES = {
    'SearchSpider.middlewares.MyMiddleware': 2
}
# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    #  'scrapy.extensions.telnet.TelnetConsole': None,
    'SearchSpider.Modules.RecordProNumExtension.RecordProNumEx': 500,
    'SearchSpider.Modules.RedisSpiderClosedExension.RedisSpiderClosedEx': 300
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #    'SearchSpider.pipelines.SearchspiderPipeline': 300,
    'SearchSpider.pipelines.ImageDealPipeline': 1,
    'SearchSpider.pipelines.SpiderTOEsPipeline': 2,
}

MYEXT_ENABLED = True
# IDLE_NUMBER = 360

SPIDER_NAME = "HfutSpider"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"

IMAGES_MIN_HEIGHT = "200"
IMAGES_MIN_WIDTH = "350"
IMAGES_URLS_FIELD = "imageUrl"


projectDir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
CONFIG_READ_SETTING = os.path.join(projectDir, 'ProcessSetting')
IMAGES_STORE = os.path.join(projectDir, 'Images')

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
