# Create your views here.

from django.shortcuts import render_to_response
from django import newforms as forms

from citeweb.citeimport import models

import re
import hashlib

import logging
import random
random.seed()

class ImportForm(forms.Form):
    url_field = forms.CharField(widget=forms.Textarea(attrs={'cols':'100', 'rows':'10', }))

def parse_urls(s):
    s = re.sub(r"\r?\n", " ", s)
    papers = re.findall(r"viewType=fullRecord.*?>(.*?)</a>", s)
    urls = re.findall(r"http://rss.isiknowledge.com/rss\?e=\w*&(?:amp;)?c=\w*", s)
    urls = [ url.replace("&amp;", "&") for url in urls ]

    # logging.info(str(urls))
    # logging.info("\n".join(papers))
    # logging.info("%d %d" % (len(urls), len(papers)))

    # if len(urls) != len(papers):
    #     # logging.debug(s)
    #     pass

    if not papers and len(s.split("\n")) == len(urls):
        papers = re.findall(r"^(.*?) : http://", s, re.M)

    return (papers, urls)

def index(request):

    urls = ()

    if request.POST:
        
        # logging.info(str(request.POST)[:100])
        
        (papers, urls) = parse_urls(request.POST["url_field"])
        url_hash = hashlib.sha1("\n".join(urls)).hexdigest()
        
        if not models.URLList.objects.filter(url_hash = url_hash):
            url_list = models.URLList.objects.create(url_hash = url_hash, urls = "\n".join(urls), papers = "\n".join(papers))
    
        paper_urls = []
        
        for (paper, url) in zip(papers, urls):
            paper_urls.append( { "paper": paper, "url" : url })

    return render_to_response('import.html', locals())

