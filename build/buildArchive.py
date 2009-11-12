#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import codecs
import string
from renderer import *

page_size = 10

def outputPost(f):
    return renderPost(f, "archive-post")

def generatePostList():
    for root, dirs, files in os.walk("posts"):
        for filename in files:
            f = os.path.join(root, filename)
            if f.endswith(".control"):
                yield f

def paginate(posts):
    pages = []
    
    def _paginate(posts):
        if len(posts) > 0:
            pages.append(map(outputPost, posts[0:page_size]))
            _paginate(posts[page_size:])
    
    _paginate(posts)
    return pages

def outputArchivePage(page):
    outstr = ""
    for p in page:
        outstr = outstr + p
    return renderArchive(outstr, "archive")

def main():
    page_no = 1
    posts = list(generatePostList())
    posts.sort()
    posts.reverse()
    
    for page in map(outputArchivePage, paginate(posts)):
        if page_no == 1:
            outputFilename = os.path.join("output","archive.html")
        else:
            outputFilename = os.path.join("output","archive-%(page)d.html" % {'page' : page_no})
        out = codecs.open(outputFilename, encoding='utf-8', mode='w+')
        out.write(page.decode("utf-8", "ignore"))
        out.close()
        print "Built archive page " + outputFilename + " (%(s)d bytes)" % {'s': os.stat(outputFilename).st_size}
        page_no += 1

if __name__ == "__main__":
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    main()