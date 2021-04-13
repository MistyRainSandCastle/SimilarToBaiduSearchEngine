import re
import random
import hashlib


def RandomStr(randLength=5):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(randLength):
        str += chars[random.randint(0, length)]
    return str


def GetMd5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

def UrlChange(url):
    url = url.split("://")
    url = url[1] if len(url) > 1 else url[0]
    url = url.replace("/", ConstValue['BACKLASH'])
    url = url.replace("?", ConstValue['QUEST'])
    return url

def UrlConvert(url):
    url=UrlChange(url)
    randStr = RandomStr()
    return url + randStr


def ChangeLabelText(str):
    return re.sub('[\n\r\t ]', '', str)


def GetLinkText(xpathLink):
    return ChangeLabelText("".join(xpathLink.xpath('./text()').getall())) or \
           ChangeLabelText(xpathLink.attrib.get('title', '')) or ChangeLabelText(
        "".join(xpathLink.xpath('.//text()').getall()))


def WebUrlType(url):
    RE_NOT_VISIT_MATCH = ".*/page\..*|.*guestbook\.asp.*|.*news\.hfut\.edu\.cn/info/\d*/\d*\..{0,5}$|.*/show-\d+-\d+-\d+\..{0,5}$|.*/\d+-[-\d]+\d+$|.*/print-[-\d]+\d+\..{0,5}$"
    INDEXURL = '.*main.{0,6}$|.*index.{0,6}$|.*cn/?$'
    LISTURL = ".*list.*|.*index.*|.*main.*"
    if not re.match(RE_NOT_VISIT_MATCH, url) == None:
        return WEBPAGETYPE['CONTENTPAGE']
    if not re.match(INDEXURL, url) == None:
        return WEBPAGETYPE['INDEXPAGE']
    if not re.match(LISTURL, url) == None:
        return WEBPAGETYPE['LISTPAGE']
    return WEBPAGETYPE['NONE']


def WebPageType(response):
    try:
        urlType = WebUrlType(response.url)
        if urlType == WEBPAGETYPE['CONTENTPAGE']:
            return WEBPAGETYPE['CONTENTPAGE']
        if urlType == WEBPAGETYPE['INDEXPAGE']:
            return WEBPAGETYPE['INDEXPAGE']
        linkList = []
        otherList = []
        for item in response.xpath('//body//a'):
            linkText = GetLinkText(item)
            if linkText:
                linkList.append(linkText)
        otherLabelList = response.xpath(
            '//body//*[name(.)!="a" and name(.)!="script" and name(.)!="style" and name(.)!="img"]')
        for item in otherLabelList:
            if not len(item.xpath("./ancestor::a")):
                otherText = ChangeLabelText("".join(item.xpath('./text()').getall()))
                if otherText:
                    otherList.append(otherText)
        linkLen = len(linkList)
        otherLen = len(otherList)
        validLinkText = "".join(linkList)
        validOtherText = "".join(otherList)
        linkTextLen = len(validLinkText)
        otherTextLen = len(validOtherText)
        signCount = len(re.findall(r'。', validOtherText))
        if not linkLen or not linkTextLen:
            return WEBPAGETYPE['CONTENTPAGE']
        elif not otherLen or not otherTextLen:
            return WEBPAGETYPE['INDEXPAGE']
        else:
            if urlType == WEBPAGETYPE['LISTPAGE']:
                return WEBPAGETYPE[
                    'CONTENTPAGE'] if linkLen / otherTextLen <= 0.1 and signCount >= 5 and otherTextLen / linkTextLen >= 1.5 else \
                    WEBPAGETYPE['INDEXPAGE']
            return WEBPAGETYPE[
                'CONTENTPAGE'] if linkLen / otherTextLen <= 0.3 and signCount >= 3 and otherTextLen / linkTextLen >= 1 else \
                WEBPAGETYPE['INDEXPAGE']
    except:
        return WEBPAGETYPE['NONE']


WEBPAGETYPE = {
    'INDEXPAGE': 'index',
    'CONTENTPAGE': 'content',
    'LISTPAGE': 'list',
    'NONE': 'none'
}

ConstValue = {
    'MAX_HEIGHT': 800,
    'MAX_WIDTH': 1100,
    'imageUrl': 'imageUrl',
    'RE_SORT_MATCH': '.*//(.*\.hfut\.edu\.cn).*',
    'BACKLASH': '+Z_*-',
    'QUEST': '*+Y_-'
}
EXTRACT_IFNO = {
    'USELESS_TAG': ['style', 'script', 'link', 'video', 'iframe', 'source', 'picture', 'header', 'blockquote',
                    'noscript', 'br', 'None', 'img', 'meta'],
    'LINK': 'a',
    'CONTENT': 'p',
    'NONE': 'None',
    'SIGNSET': r'''！|，|。|？|、|；|：|“|”|‘|’|《|》|（|）|,|\.|\?|:|;|'|"|!|\(|\)'''
}