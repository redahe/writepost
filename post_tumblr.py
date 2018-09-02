#!/usr/bin/python

import urllib
import os
import subprocess
import conf

SHARE_LINK='http://tumblr.com/widgets/share/tool?canonicalUrl='

def post(path):
    link = None
    title = None
    tags=[]
    with open(path) as f:
        data = f.readlines()
        for i in range(len(data)):
            line = data[i].strip()
            if line.startswith('http://') or line.startswith('https://'):
                link = line
            if line.startswith('#+'):
                data[i] = ''
            if line.startswith('#+TITLE:'):
                title=line[8:]
            if line.startswith('#+TAGS:'):
                tags=line[7:].split()
    if not link:
        link = 'http://tumblr.com'
    text=''.join(data)
    new_link=(SHARE_LINK + link + '&posttype=text&content=' + urllib.quote_plus(text))
    if title:
        new_link = new_link + '&title='+urllib.quote_plus(title)
    if tags:
        new_link = new_link+'&tags='+','.join(tags)
    print new_link

    os.system(conf.run_browser+' "'+new_link+'"')
    return True



