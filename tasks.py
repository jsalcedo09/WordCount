import logging
import urllib
import re
from google.appengine.ext import deferred
from google.appengine.api import memcache
from google.appengine.api import channel
import json


def read_web_site(url, deep, words, search_id,visited = list()):
    deep -= 1
    visited.append(url)
    increment_links(search_id,1)
    information = {'links':memcache.get('%s-links' % search_id),
                   'words':{}}

    logging.info("Searching for links in %s", url)

    if deep >= 0:
        req = urllib.urlopen(url)
        encoding=req.headers['content-type'].split('charset=')[-1]
        try:
            html = unicode(req.read(), encoding)
            for word in words.split(','):
                word_count = html.count(word)
                if word_count:
                    increment_word(search_id, word_count, word)


            for link in find_links(html):
                if link.startswith('http') and link not in visited:
                    deferred.defer(read_web_site, link, deep, words, search_id, visited)
        except LookupError:
            logging.warn("Invalid ecoding %s", encoding)


    for word in words.split(','):
        information['words'].update({word:memcache.get("%s-word-%s" % (search_id, word))})

    channel.send_message("%s-search" % search_id, json.dumps(information))




def find_links(html):
    return re.findall(r'href=[\'"]?([^\'" >]+)', html)

def increment_links(search_id, number):
    memcache.incr("%s-links" % search_id, delta=number, initial_value=0)

def increment_word(search_id, number,word):
    memcache.incr("%s-word-%s" % (search_id, word), delta=number, initial_value=0)
