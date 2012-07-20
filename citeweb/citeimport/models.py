from django.db import models

class Paper(models.Model):
    # turns out we need to store when each paper was created, as WOS returns old papers if there are no new papers
    key = models.CharField(max_length=255, primary_key=True)
    created = models.DateTimeField(auto_now=True)

class URLList(models.Model):
    # the URL hash is computed from the list of URLs and is used to retrieve this list
    url_hash = models.CharField(max_length=255)
    urls = models.TextField()
    papers = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

class CachedURL(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    papers = models.TextField()
    created = models.DateTimeField(auto_now=True)
    
class UserPrefs(models.Model):
    user = models.CharField(max_length=255)
    url_hash = models.CharField(max_length=255)
    # the user hash is computed once from some entropy and then provides a stable link for the user
    user_hash = models.CharField(max_length=255)
    
    
    
    