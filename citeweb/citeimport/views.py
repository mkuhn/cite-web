# Create your views here.

from django.shortcuts import render_to_response
from django import newforms as forms

from citeweb.citeimport import models

import re
import hashlib

class ImportForm(forms.Form):
    url_field = forms.CharField(widget=forms.Textarea(attrs={'cols':'100', 'rows':'10', }))

def parse_urls(s):
    return re.findall(r"http://rss.isiknowledge.com/rss\?e=\w*&c=\w*", s)
    

def index(request):

    if request.POST:
        urls = parse_urls(request.POST["url_field"])
        url_hash = hashlib.sha1("\n".join(urls)).hexdigest()
        
        if not models.URLList.all().filter("url_hash = ", url_hash).get():
            url_list = models.URLList(url_hash = url_hash, urls = urls)
            url_list.put()
    
    if urls:
        f = ImportForm(data = { "url_field" : "\n".join(urls) } )
        
    else:
        f = ImportForm()
    
    return render_to_response('index.html', locals())

