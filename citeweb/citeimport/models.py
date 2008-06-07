from django.db import models

class URLList(models.Model):
    # the URL hash is computed from the list of URLs and is used to retrieve this list
    url_hash = models.CharField(maxlength=255)
    urls = models.TextField()
    papers = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
class CachedURL(models.Model):
    url = models.CharField(maxlength=255)
    title = models.CharField(maxlength=255)
    papers = models.TextField()
    created = models.DateTimeField(auto_now=True)
    
class UserPrefs(models.Model):
    user = models.CharField(maxlength=255)
    url_hash = models.CharField(maxlength=255)
    # the user hash is computed once from some entropy and then provides a stable link for the user
    user_hash = models.CharField(maxlength=255)
    
    
    
    