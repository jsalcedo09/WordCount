from google.appengine.ext import ndb

class Counts(ndb.Model):
    links_count = ndb.IntegerProperty()
    words_count = ndb.IntegerProperty()



