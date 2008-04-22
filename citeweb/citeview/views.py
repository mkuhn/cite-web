# Create your views here.

from django.shortcuts import render_to_response
from django import newforms as forms

from citeweb.citeimport import models

from google.appengine.api import urlfetch

import re
import hashlib

import datetime
from BeautifulSoup import BeautifulStoneSoup

import logging

def cache_url(url):
    
    cached_url = models.CachedURL().all().filter("url = ", url).get()
    
    if not cached_url or cached_url.created < datetime.datetime.utcnow() - datetime.timedelta(hours = 1):
        
        r = urlfetch.fetch(url)

        soup = BeautifulStoneSoup(r.content, selfClosingTags=['br'])
    
        title = str(soup.find("title").string)
    
        papers = []
    
        for item in soup.findAll("item"):
        
            p_link = str(item.link.string)
            p_title, _, p_authors, _, p_citation = [ str(t.string) for t in item.description.contents ]
        
            p = "\n".join((p_link, p_title, p_authors, p_citation))
            papers.append(p)

        if not cached_url:
            cached_url = models.CachedURL(url = url, title = title, papers = papers)
        else:
            cached_url.url      = url      
            cached_url.title    = title    
            cached_url.papers   = papers   
            
            
        cached_url.put() 
        return r.content


def index(request, url_hash):

    url_list = models.URLList.all().filter("url_hash = ", url_hash).get()
    
    for url in url_list.urls:
        s = cache_url(url)
    
    s = ""
    
    
    return render_to_response('view_index.html', locals())

