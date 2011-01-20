# Create your views here.

from django.shortcuts import render_to_response
from django import newforms as forms

from citeweb.citeimport import models

import re
import hashlib

import logging
import random
random.seed()

import htmlentitydefs

class ImportForm(forms.Form):
    url_field = forms.CharField(widget=forms.Textarea(attrs={'cols':'100', 'rows':'10', }))

def convert_html_entities(s):
    matches = re.findall("&#\d+;", s)
    if len(matches) > 0:
        hits = set(matches)
        for hit in hits:
                name = hit[2:-1]
                try:
                        entnum = int(name)
                        s = s.replace(hit, unichr(entnum))
                except ValueError:
                        pass

    matches = re.findall("&\w+;", s)
    hits = set(matches)
    amp = "&amp;"
    if amp in hits:
        hits.remove(amp)
    for hit in hits:
        name = hit[1:-1]
        if htmlentitydefs.name2codepoint.has_key(name):
                s = s.replace(hit, unichr(htmlentitydefs.name2codepoint[name]))
    s = s.replace(amp, "&")
    return s
    
def parse_urls(s):
    
    s = s.strip()
    s = re.sub(r"\r?\n", " ", s)
    if s.startswith("&lt;"): s = convert_html_entities(s)
    
    papers = [ x for x in re.findall(r"viewType=fullRecord&(?:amp;)?UT.*?>([^<>]*?)</a>", s) if x.strip() ]
    urls = re.findall(r"http://rss.isiknowledge.com/rss\?e=\w*&(?:amp;)?c=\w*", s)
    urls = [ url.replace("&amp;", "&") for url in urls ]

    # logging.info(s)
    # logging.info(str(urls))
    # logging.info("\n".join(papers))
    # logging.info("%d %d" % (len(urls), len(papers)))

    if len(urls) != len(papers):
         logging.debug(s)
         pass

    assert len(urls) == len(papers)
    assert all( "<" not in s and ">" not in s for s in papers )

    return (papers, urls)

def index(request):

    urls = ()

    if request.POST:

        (papers, urls) = parse_urls(request.POST["url_field"])
        url_hash = hashlib.sha1("\n".join(urls)).hexdigest()
        proposed_user_hash = hashlib.sha1(url_hash + str(random.random())).hexdigest()
        
        if not models.URLList.objects.filter(url_hash = url_hash):
            url_list = models.URLList.objects.create(url_hash = url_hash, urls = "\n".join(urls), papers = "\n".join(papers))
    
        paper_urls = []
        
        for (paper, url) in zip(papers, urls):
            paper_urls.append( { "paper": paper, "url" : url })

    return render_to_response('import.html', locals())

def save(request):
    
    if request.GET:
        
        url_hash = request.GET.get("url_hash")
        user_hash = request.GET.get("user_hash")
        
        if len(user_hash) >= 40:
            
            userprefs_l = models.UserPrefs.objects.filter(user_hash = user_hash)
            
            if not userprefs_l:
                # if this is a new user, generate a hash and store the data
                userprefs = models.UserPrefs(user = user_hash, user_hash = user_hash, url_hash = url_hash)
            
            else:
                # if it is old, leave the user hash unchanged and just adapt the url hash
                userprefs = userprefs_l[0]
                userprefs.url_hash = url_hash
            
            userprefs.save()
            
    return render_to_response('save.html', locals())

            
        