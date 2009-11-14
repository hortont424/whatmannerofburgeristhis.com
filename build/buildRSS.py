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

def generateRSSFeed(posts, outputFilename, title=u"hortont &middot; blog"):
    posts.sort()
    posts.reverse()
    posts = posts[0:settings.page_size]
    
    output = ""
    
    for p in posts:
        output += renderPost(p, "rss-post", True)
    
    page = renderArchive(output, "rss", None, None, True, title)
    
    if not os.path.exists(os.path.dirname(outputFilename)):
        os.makedirs(os.path.dirname(outputFilename))
    
    out = codecs.open(outputFilename, encoding='utf-8', mode='w+')
    out.write(page.decode("utf-8", "ignore"))
    out.close()
    print "Built syndication feed " + outputFilename + " (%(s)d bytes)" % {'s': os.stat(outputFilename).st_size}

if __name__ == "__main__":
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    generateRSSFeed(generatePostList("posts"), os.path.join("output", "feed", "rss.xml"))
    
    categoryMap = generateCategoryMap("posts")
    
    for cat in categoryMap:
        generateRSSFeed(categoryMap[cat], os.path.join("output", "topics", settings.categoryURLFromName(cat), "feed", "rss.xml"), u"hortont &middot; blog &middot; " + cat)