import logging
import urllib
import re
from google.appengine.ext import deferred


def read_web_site(url,deep, words, visited = list()):
    deep -= 1
    visited.append(url)
    logging.info("Searching for links in %s", url)
    if deep >= 0:
        html = urllib.urlopen(url).read()
        for link in find_links(html):
            if link.startswith('http') and link not in visited:
                deferred.defer(read_web_site, link, deep, words, visited)
    else:
        pass

def find_links(html):
    return re.findall(r'href=[\'"]?([^\'" >]+)', html)

