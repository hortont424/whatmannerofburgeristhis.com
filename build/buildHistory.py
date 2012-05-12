#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import codecs
import string
from renderer import *
from build import *
from settings import *
from collections import defaultdict

def historyFromPages(pages):
    outPages = defaultdict(list)
    lastYear = 0

    for page in pages:
        metadata = json.loads(readFileContents(page), encoding='utf-8')

        try:
            metadata["categories"] = joinCategoryList(resolveCategoryList(metadata["categories"]))
        except:
            metadata["categories"] = ""

        pubDate = metadata["date"]

        if "post-name" not in metadata:
            metadata["post-name"] = generatePostName(metadata["title"])

        metadata["url"] = os.path.join(blog_prefix, metadata["post-name"])

        metadata["id"] = re.sub("[^0-9]", "", metadata["date"])
        metadata["date"] = datetime.datetime.strptime(pubDate, "%Y.%m.%d %H:%M:%S").strftime("%Y.%m.%d")

        thisYear = datetime.datetime.strptime(pubDate, "%Y.%m.%d %H:%M:%S").year

        outPages[thisYear].append(metadata)

    return outPages

def generateHistory(posts, outputLocation, category=None):
    page_no = 1
    posts.sort()
    posts.reverse()

    page = renderHistory(historyFromPages(posts), "history")

    outputFilename = os.path.join(outputLocation, "history", "index.html")

    if not os.path.exists(os.path.dirname(outputFilename)):
        os.makedirs(os.path.dirname(outputFilename))

    out = codecs.open(outputFilename, encoding='utf-8', mode='w+')
    out.write(page.decode("utf-8", "ignore"))
    out.close()
    print outputFilename.replace(os.path.join("output", ""), "") + " (index, %(s)d bytes)" % {'s': os.stat(outputFilename).st_size}


if __name__ == "__main__":
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    generateHistory(generatePostList("posts"), os.path.join("output", blog_dir))
