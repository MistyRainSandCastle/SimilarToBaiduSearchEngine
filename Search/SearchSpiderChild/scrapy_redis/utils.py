import re
import six


def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if six.PY3 and isinstance(s, bytes):
        return s.decode(encoding)
    return s


def jump_url(url):
    RE_NOT_VISIT_MATCH = ".*news\.hfut\.edu\.cn/yzhy\.jsp\?urltype=tree.TreeTempUrl.*"
    res = re.match(RE_NOT_VISIT_MATCH, url)
    return not res == None
