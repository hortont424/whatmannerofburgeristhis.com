import os
import sys
import string
from renderer import *

def generatePostList(type):
    posts = []
    for root, dirs, files in os.walk(type):
        for filename in files:
            f = os.path.join(root, filename)
            if f.endswith(".control"):
                posts.append(f)
    return posts

def buildBackwardsCompatibilityLinks(type):
    posts = {}
    for root, dirs, files in os.walk(type):
        for filename in files:
            f = os.path.join(root, filename)
            if not f.endswith(".control"):
                continue
            
            metadata = json.loads(readFileContents(f), encoding='utf-8')
            
            if "post-name" not in metadata:
                continue
            
            ourDate = datetime.datetime.strptime(metadata["date"], "%Y.%m.%d %H:%M:%S").strftime("%Y/%m") # TODO: fixed slash
            outputFolder = os.path.join("output", ourDate, metadata["post-name"])
            
            if not os.path.exists(outputFolder):
                os.makedirs(outputFolder)
            
            outputFile = os.path.join(outputFolder, ".htaccess")
            realURL = os.path.join(www_prefix, "posts", f.replace(".control", ".html").replace("posts" + "/", ""))
            htaccessContents = "RewriteEngine on\n" + "RewriteRule ^.*$ " + realURL + "\n"
            out = codecs.open(outputFile, mode="w+")
            out.write(htaccessContents)
            out.close()

def generateCategoryMap(type):
    posts = {}
    for root, dirs, files in os.walk(type):
        for filename in files:
            f = os.path.join(root, filename)
            if not f.endswith(".control"):
                continue
            
            metadata = json.loads(readFileContents(f), encoding='utf-8')
            
            if "categories" not in metadata:
                continue
            
            for cat in metadata["categories"]:
                if cat not in posts:
                    posts[cat] = []
                posts[cat].append(f)
    return posts

def buildPosts(dir, template, typeName, outDir):
    for filename in generatePostList(dir):
        page = renderPost(filename, template)
        outputFilename = os.path.join("output", outDir, filename.replace(".control", ".html").replace(dir + "/", ""))

        if not os.path.exists(os.path.dirname(outputFilename)):
            os.makedirs(os.path.dirname(outputFilename))

        out = codecs.open(outputFilename, encoding='utf-8', mode='w+')
        out.write(page.decode("utf-8", "ignore"))
        out.close()
        print "Built " + typeName + " " + outputFilename + " (%(s)d bytes)" % {'s': os.stat(outputFilename).st_size}