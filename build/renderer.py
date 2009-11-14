#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import datetime
import os
import json
import codecs
import string
import re
import sys
from genshi.template import TemplateLoader
from genshi.core import Markup
from settings import *

loader = TemplateLoader('templates', variable_lookup='lenient')

def readFileContents(fn):
    fileHandle = codecs.open(fn, encoding='utf-8')
    fileContents = unicode(fileHandle.read())
    fileHandle.close()
    return fileContents

def joinCategoryList(cats):
    if len(cats) <= 2:
        return string.join(cats, " and ")
    else:
        return string.join(cats[:-2], ", ") + ", " + string.join(cats[-2:], ", and ")

def renderPost(f, template, rss=False):
    metadata = json.loads(readFileContents(f), encoding='utf-8')
    contents = readFileContents(f.replace(".control",""))
    contents = contents.replace("\n","\n<br/>")
    
    if template == "":
        template = metadata["template"]
    
    try:
        metadata["categories"] = joinCategoryList(metadata["categories"])
    except:
        metadata["categories"] = ""
    
    metadata["content"] = contents
    
    pubDate = metadata["date"]
    
    metadata["url"] = w(f.replace(".control",""))
    metadata["id"] = re.sub("[^0-9]", "", metadata["date"])
    metadata["date"] = datetime.datetime.strptime(pubDate, "%Y.%m.%d %H:%M:%S").strftime("%Y.%m.%d")
    
    metadata["shortContent"] = re.sub("<(.*?)>","",contents[0:500]) + "..."
    
    if "pubDate" not in metadata:
        metadata["pubDate"] = datetime.datetime.strptime(pubDate, "%Y.%m.%d %H:%M:%S").strftime("%a, %d %b %Y %H:%M:%S +0000")

    if "guid" not in metadata:
        metadata["guid"] = metadata["url"]
    
    try:
        comments = metadata["comments"]
    except:
        metadata["comments"] = []
    
    postfix = doctype = "html"
    if rss:
        postfix = "xml"
        doctype = None
    
    tmpl = loader.load(template + '.' + postfix, encoding='utf-8')
    return tmpl.generate(post=metadata, baseurl=www_prefix).render(postfix, doctype=doctype)

def renderArchive(c, template, next, prev, rss=False, title=u"hortont &middot; blog"):
    postfix = doctype = "html"
    if rss:
        postfix = "xml"
        doctype = None
    
    buildDate = datetime.datetime.today().strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    showTitle = (title != u"hortont &middot; blog")
    
    tmpl = loader.load(template + '.' + postfix, encoding='utf-8')
    return tmpl.generate(content=c.decode("utf-8","ignore"),
                         baseurl=www_prefix,
                         nextPage=next,
                         previousPage=prev,
                         buildDate=buildDate,
                         title=title,
                         showTitle=showTitle).render(postfix, doctype=doctype)