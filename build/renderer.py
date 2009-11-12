#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import json
import codecs
import string
import re
import sys
from genshi.template import TemplateLoader
from genshi.core import Markup
from settings import *

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

def renderPost(f, template):
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
    
    metadata["url"] = w(f.replace(".control",""))
    metadata["id"] = re.sub("[^0-9]", "", metadata["date"])
    
    loader = TemplateLoader('templates', variable_lookup='lenient')
    tmpl = loader.load(template + '.html', encoding='utf-8')
    return tmpl.generate(post=metadata).render('html', doctype='html')

def renderArchive(c, template):
    loader = TemplateLoader('templates', variable_lookup='lenient')
    tmpl = loader.load(template + '.html', encoding='utf-8')
    return tmpl.generate(content=c.decode("utf-8","ignore"), baseurl=w("")).render('html', doctype='html')