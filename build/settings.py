import os

page_size = 10
www_prefix = "http://hortont.com/"

if os.uname()[1] == "Kaylee.local":
    www_prefix = "http://localhost/~hortont/output/"

blog_dir = "blog/"

blog_prefix = www_prefix + blog_dir

def w(u):
    return www_prefix + u

def categoryURLFromName(n):
    if n == "gnome":
        return "code/gnome"
    if n == "fooding":
        return "personal/fooding"
    if n == "video":
        return "school/video"
    return n

def categoryDisplayName(n):
    return n.replace("-"," ")