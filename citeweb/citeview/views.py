# Create your views here.

from django.shortcuts import render_to_response
from django import newforms as forms
from django.http import HttpResponse

from citeweb.citeimport import models

import urllib

import re
import hashlib
import itertools 

import sys

from collections import defaultdict
import datetime

from BeautifulSoup import BeautifulStoneSoup
import PyRSS2Gen

import logging

def cache_url(url):
    
    cached_url = models.CachedURL.objects.filter(url = url)
    if cached_url:
        cached_url = cached_url[0] 
    
    now = datetime.datetime.utcnow()
    
    # only load now URLs or those downloaded more than 1 hours ago
    if not cached_url or cached_url.created < now - datetime.timedelta(hours = 1):
        
        print >> sys.stderr, url
        
        r = urllib.urlopen(url)

        soup = BeautifulStoneSoup(r, selfClosingTags=['br'])

        title = str(soup.find("title").string)
    
        papers = []
    
        for item in soup.findAll("item"):
        
            p_link = str(item.link.string)
            p_title, _, p_authors, _, p_citation = [ str(t.string) for t in item.description.contents ]
        
            p = "\t".join((p_link, p_title, p_authors, p_citation))
            papers.append(p)

        if not cached_url:
            cached_url = models.CachedURL.objects.create(url = url, title = title, papers = "\n".join(papers), created = now)
        else:
            cached_url.url      = url      
            cached_url.title    = title    
            cached_url.papers   = "\n".join(papers)
            cached_url.created  = now
            
            cached_url.save() 
    
    return cached_url


def papers_to_rss(request, url_hash, papers):
 
    now = datetime.datetime.now()
    
    def rss_for_paper(paper):
        
        paper["citing_list"] = "</li><li>".join(paper["citing"])
         
        html = """
<p>%(authors)s<br/>%(citation)s</p>
<ul><li>%(citing_list)s</li></ul>
<p>Search: <a href="http://scholar.google.com/scholar?q=%(search_param)s">Google Scholar</a> &ndash; <a href="%(wos_url)s">WOS</a> &ndash; <a href="http://www.google.com/search?q=%(search_param)s">Google</a><br>
</p>""" % paper

        url = "http://scholar.google.com/scholar?q=%s" % paper["scholar_param"]
        
        return PyRSS2Gen.RSSItem(
            title = paper["title"],
            description = html,
            link = url,
            guid = PyRSS2Gen.Guid(url),
            pubDate = now
        )
        
    
    rss = PyRSS2Gen.RSS2(
        title = "CiteWeb citation feed",
        link = "http://%s/view/%s/" % (request.META["SERVER_NAME"], url_hash),
        description = "CiteWeb aggregates your ISI Web Of Science citation alerts.",

        lastBuildDate = now,

        items = [ rss_for_paper(paper) for paper in papers ]
    )

    return rss.to_xml()
    
    
def index(request, stable = False, url_hash = "", rss = False):

    rss_url = "rss.xml"

    #TODO
    # # if we come via a stable URL, get the URL hash from the stored users
    # if stable:
    #     url_hash = models.UserPrefs.objects.filter(user_hash, url_hash).get().url_hash

    #TODO
    # user = users.get_current_user()
    # if user:
    #     nickname = user.nickname()
    #     logout_url = users.create_logout_url("/")
    # 
    # # if there are no parameters, see if the user is logged in and has an associated URL
    # if not url_hash:
    #     userprefs = models.UserPrefs.objects.filter(user = user).get()
    #     
    #     if userprefs:
    #         url_hash = userprefs.url_hash
    #         rss_url = "/view/stable/%s/rss.xml" % userprefs.user_hash
        
    # okay, we can't find a URL hash: tell the user to import something
    if not url_hash:
        from citeweb.citeimport import views
        return views.index(request)



    url_list = models.URLList.objects.filter(url_hash = url_hash)[0]
    
    error_message = ""
    
    if not url_list:
        
        error_message = "Sorry, I could not find an associated list of URLs to your query."
    
    else:
    
        urls = url_list.urls.split("\n")
        papers = url_list.papers.split("\n")
        
        logging.info("%d %d" % (len(urls), len(papers)))
    
        url2title = {}
        for (url, title) in zip(urls, papers):
            url2title[url] = title
    
        paper2citing = defaultdict(list)
    
        for url in urls:
            cached_url = cache_url(url)
            title = url2title[url]
            
            cited_papers = cached_url.papers
            
            if not cited_papers:
                continue 

            for paper in cited_papers.split("\n"):
                paper2citing[paper].append( title )

        papers = []
                
        for (paper, citing) in sorted(paper2citing.items()):
            (wos_url, title, authors, citation) = paper.split("\t")

            short_title = re.sub(" ((the|and|or|for|to|in|of|an?|is|it|-+) )+", " ", title)

            search_param = "%s %s" % (authors[:authors.index(",")], short_title)
            scholar_param = ("allintitle%%3A %s author%%3A%s" % (short_title, authors[:authors.index(",")], )).replace(" ", "+")
            papers.append({ "wos_url" : wos_url, "scholar_param" : scholar_param, "search_param" : search_param, "title" : title, "authors" : authors, "citation" : citation, "citing" : citing })
    
    
        
    if rss:
        return HttpResponse(papers_to_rss(request, url_hash, papers), mimetype="application/rss+xml")
    else:    
        return render_to_response('view_index.html', locals())

