from google.appengine.ext import ndb


class Book(ndb.Model):
    name = ndb.StringProperty()
    blob_id = ndb.BlobKeyProperty()
