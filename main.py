import os
import random
from google.appengine.ext import deferred
from google.appengine.api import channel, users, memcache
import jinja2
import webapp2
from tasks import read_web_site
import string

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        string.letters
        context = {'search_id':''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))}
        template = jinja_environment.get_template('index.html')
        self.response.write(template.render(context))

    def post(self):
        context = dict()

        context['url'] = self.request.POST.get("url")
        context['search_id'] = self.request.POST.get("search_id")
        context['deep'] = int(self.request.POST.get("deep"))
        context['words'] = self.request.POST.get("words")

        #Clear counters
        memcache.set('%s-links' % context['search_id'], 0)
        for word in context['words'].split(','):
            memcache.set("%s-word-%s" % (context['search_id'], word),0)

        deferred.defer(read_web_site, **context)

        context['token'] = channel.create_channel("%s-search" % context['search_id'])

        template = jinja_environment.get_template('index.html')
        self.response.write(template.render(context))

app = webapp2.WSGIApplication([('/', MainHandler),
                              ], debug=True)
