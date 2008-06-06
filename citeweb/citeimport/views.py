# Create your views here.

from django.shortcuts import render_to_response
from django import newforms as forms

from citeweb.citeimport import models

import re
import hashlib

class ImportForm(forms.Form):
    url_field = forms.CharField(widget=forms.Textarea(attrs={'cols':'100', 'rows':'10', }))

def parse_urls(s):
    papers = re.findall(r"viewType=fullRecord.*?<p>(.*?)</a></td>", s)
    urls = re.findall(r"http://rss.isiknowledge.com/rss\?e=\w*&c=\w*", s)

    if not papers and len(s.split("\n")) == len(urls):
        papers = re.findall(r"^(.*?) : http://", s, re.M)

    return (papers, urls)

def index(request):

    urls = ()

    if request.POST:
        (papers, urls) = parse_urls(request.POST["url_field"])
        url_hash = hashlib.sha1("\n".join(urls)).hexdigest()
        
        if not models.URLList.all().filter("url_hash = ", url_hash).get():
            url_list = models.URLList(url_hash = url_hash, urls = urls, papers = papers)
            url_list.put()
    
    if urls:
        f = ImportForm(data = { "url_field" : "\n".join( "%s : %s" % (p, u) for (p, u) in zip(papers,urls)) } )
        
    else:
        f = ImportForm()
    
    return render_to_response('index.html', locals())

