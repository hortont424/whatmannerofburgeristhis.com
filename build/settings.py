import os

page_size = 10

www_prefix = "http://www.whatmannerofburgeristhis.com/"
static_prefix = "http://files.whatmannerofburgeristhis.com/www/"

# Set this to the path that you keep your local copy in, and where it's served
# to (this should point to the output directory)
if os.getcwd() == "/Users/hortont/src/whatmannerofburgeristhis.com":
    www_prefix = "file:///Users/hortont/src/whatmannerofburgeristhis.com/output/"
    static_prefix = "file:///Users/hortont/src/whatmannerofburgeristhis.com/output/"

blog_dir = "blog/"

blog_prefix = www_prefix + blog_dir

def w(u):
    return www_prefix + u

# Set up a hierarchy for categories here. I think this is mostly just for URLs
# but I really don't remember.
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