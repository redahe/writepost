#!/usr/bin/python

import facebook
import urllib
import os


SHARE_LINK='https://www.facebook.com/sharer/sharer.php?u='


def post(path):
    link = None
    with open(path) as f:
        data = f.readlines()
        for i in range(len(data)):
            line = data[i].strip()
            if line.startswith('http://') or line.startswith('https://'):
                link = line
                data[i] = ''
            if line.startswith('#+'):
                data[i] = ''
        if not(link):
            print('To be shared on Facebook the post must contain a link on a separate line.')
            return False
    quote=''.join(data)
    new_link=(SHARE_LINK + link + '&quote=' + urllib.quote_plus(quote))
    os.system('google-chrome -app="'+new_link+'"')
    print('Browser was closed, assume the post was shared')
    return True



