from google.appengine.ext import db

class URLList(db.Model):
    url_hash = db.StringProperty()
    urls = db.StringListProperty()
    papers = db.StringListProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    
class CachedURL(db.Model):
    url = db.StringProperty()
    title = db.StringProperty()
    papers = db.StringListProperty()
    created = db.DateTimeProperty(auto_now=True)
    