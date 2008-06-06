from google.appengine.ext import db

class URLList(db.Model):
    # the URL hash is computed from the list of URLs and is used to retrieve this list
    url_hash = db.StringProperty()
    urls = db.StringListProperty()
    papers = db.StringListProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    
class CachedURL(db.Model):
    url = db.StringProperty()
    title = db.StringProperty()
    papers = db.StringListProperty()
    created = db.DateTimeProperty(auto_now=True)
    
class UserPrefs(db.Model):
    user = db.UserProperty()
    url_hash = db.StringProperty()
    # the user hash is computed once from some entropy and then provides a stable link for the user
    user_hash = db.StringProperty()
    
    
    
    