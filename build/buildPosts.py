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
    return renderPost(f, "post")

def generatePostList():
    for root, dirs, files in os.walk("posts"):
        for filename in files:
            f = os.path.join(root, filename)
            if f.endswith(".control"):
                yield f

def main():
    posts = list(generatePostList())
    
    for filename in posts:
        page = outputPost(filename)
        outputFilename = os.path.join("output", filename.replace(".control", ".html"))
        
        if not os.path.exists(os.path.dirname(outputFilename)):
            os.makedirs(os.path.dirname(outputFilename))
        
        out = codecs.open(outputFilename, encoding='utf-8', mode='w+')
        out.write(page.decode("utf-8", "ignore"))
        out.close()
        print "Built post " + outputFilename + " (%(s)d bytes)" % {'s': os.stat(outputFilename).st_size}

if __name__ == "__main__":
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    main()