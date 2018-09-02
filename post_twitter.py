#!/usr/bin/python

import urllib
import os
import subprocess
import conf

SHARE_LINK='https://twitter.com/intent/tweet?text='

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
                data[i]=''
            if line.startswith('#+'):
                data[i] = ''
            if line.startswith('#+TITLE:'):
                title=line[8:]
            if line.startswith('#+TAGS:'):
                tags=line[7:].split()
    text=''.join(data)
    new_link=(SHARE_LINK + urllib.quote_plus(text))
    if link:
        new_link = new_link+'&url='+link
    if tags:
        new_link = new_link+'&hashtags='+','.join(tags)
    print new_link

    os.system(conf.run_browser+' "'+new_link+'"')
    return True



