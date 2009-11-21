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

def outputArchivePage(page, next, prev, category):
    outstr = ""
    for p in page:
        outstr = outstr + p
    return renderArchive(outstr, "archive", next, prev, False, category)

def generateArchive(posts, outputLocation, category=None):
    page_no = 1
    posts.sort()
    posts.reverse()
    
    pages = [renderPost(f, "archive-post") for f in posts]
        
    page = outputArchivePage(pages, "", "", category)
    outputFilename = os.path.join(outputLocation, "everything", "index.html")
    
    if not os.path.exists(os.path.dirname(outputFilename)):
        os.makedirs(os.path.dirname(outputFilename))
    
    out = codecs.open(outputFilename, encoding='utf-8', mode='w+')
    out.write(page.decode("utf-8", "ignore"))
    out.close()
    print "Built everything page " + outputFilename + " (%(s)d bytes)" % {'s': os.stat(outputFilename).st_size}


if __name__ == "__main__":
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    generateArchive(generatePostList("posts"), os.path.join("output"))

    categoryMap = generateCategoryMap("posts")

    for cat in categoryMap:
        generateArchive(categoryMap[cat], os.path.join("output", "topics", settings.categoryURLFromName(cat)), cat)