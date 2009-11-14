#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import codecs
import string
from renderer import *
from build import *
import settings

def paginate(posts):
    pages = []
    
    def _paginate(posts):
        if len(posts) > 0:
            pages.append([renderPost(f, "archive-post") for f in posts[0:settings.page_size]])
            _paginate(posts[page_size:])
    
    _paginate(posts)
    return pages

def outputArchivePage(page, next, prev, title):
    outstr = ""
    for p in page:
        outstr = outstr + p
    return renderArchive(outstr, "archive", next, prev, False, title)

def filenameForPage(page_no):
    if page_no == 1:
        return "index.html"
    else:
        return "archive-%(page)d.html" % {'page' : page_no}

def generateArchive(posts, outputLocation, title=u"hortont &middot; blog"):
    page_no = 1
    posts.sort()
    posts.reverse()
    
    pages = paginate(posts)
    
    for pagination in pages:
        previousPageName = nextPageName = ""
        
        if page_no != 1:
            previousPageName = filenameForPage(page_no - 1)
        
        if page_no != len(pages):
            nextPageName = filenameForPage(page_no + 1)
        
        page = outputArchivePage(pagination, nextPageName, previousPageName, title)
        outputFilename = os.path.join(outputLocation, filenameForPage(page_no))
        
        if not os.path.exists(os.path.dirname(outputFilename)):
            os.makedirs(os.path.dirname(outputFilename))
        
        out = codecs.open(outputFilename, encoding='utf-8', mode='w+')
        out.write(page.decode("utf-8", "ignore"))
        out.close()
        print "Built archive page " + outputFilename + " (%(s)d bytes)" % {'s': os.stat(outputFilename).st_size}
        page_no += 1

if __name__ == "__main__":
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    generateArchive(generatePostList("posts"), os.path.join("output"))

    categoryMap = generateCategoryMap("posts")

    for cat in categoryMap:
        generateArchive(categoryMap[cat], os.path.join("output", "topics", settings.categoryURLFromName(cat)), u"hortont &middot; blog &middot; " + cat)