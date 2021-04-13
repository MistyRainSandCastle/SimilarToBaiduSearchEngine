# -*- coding: utf-8 -*-

from urllib import parse
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline, ImageException
from SearchSpider.Modules.CommonModule import UrlConvert, ConstValue,GetMd5,UrlChange
from PIL import Image
from scrapy_redis.pipelines import RedisPipeline
import six

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO


class SpiderTOEsPipeline(RedisPipeline):
    pass


class ImageDealPipeline(ImagesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        super(ImageDealPipeline, self).__init__(store_uri, settings=settings,
                                                download_func=download_func)
        self.imgNameDict = {}

    def get_media_requests(self, item, info):
        if ConstValue["imageUrl"] in item:
            urls = item["imageUrl"].split(',')
            return [Request(parse.urljoin(item["url"], x), meta={"domain": item["url"]}) for x in urls]

    def get_images(self, response, request, info):
        path = self.file_path(request, response=response, info=info)
        origImage = Image.open(BytesIO(response.body))
        width, height = origImage.size
        if width < self.min_width or width > ConstValue['MAX_WIDTH'] or \
                height < self.min_height or height > ConstValue['MAX_HEIGHT']:
            urlMd5=GetMd5(request.url)
            if self.imgNameDict.get(urlMd5):
                del self.imgNameDict[urlMd5]
            raise ImageException("Image not is standard size")

        image, buf = self.convert_image(origImage)
        yield path, image, buf

        for thumb_id, size in six.iteritems(self.thumbs):
            thumb_path = self.thumb_path(request, thumb_id, response=response, info=info)
            thumb_image, thumb_buf = self.convert_image(image, size)
            yield thumb_path, thumb_image, thumb_buf

    def item_completed(self, results, item, info):
        urlCom=UrlChange(item['url'] if 'url' in item else '')
        item['imageResult'] =",".join([x['path'] for ok, x in results if ok and x['path'][:-9]==urlCom])
        return item

    def file_path(self, request, response=None, info=None):
        urlMd5=GetMd5(request.url)
        imgName = self.imgNameDict.get(urlMd5)
        if not imgName:
            imgName = '%s.jpg' % (UrlConvert(request.meta.get("domain", "")))
            self.imgNameDict[urlMd5] = imgName
        return imgName
