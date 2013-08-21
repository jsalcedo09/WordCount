import logging
import os
from google.appengine.ext import deferred
import jinja2
import webapp2
from tasks import leer_sitio_web

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        context = {}


        template = jinja_environment.get_template('index.html')
        self.response.write(template.render(context))

    def post(self):
        context = {}
        context['url'] = self.request.POST.get("url")
        context['deep'] = self.request.POST.get("deep")
        context['words'] = self.request.POST.get("words")
        deferred.defer(leer_sitio_web,context['url'],int(context['deep']), context['words'])
        template = jinja_environment.get_template('index.html')
        self.response.write(template.render(context))

app = webapp2.WSGIApplication([('/', MainHandler),
                              ], debug=True)
