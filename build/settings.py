import os

www_prefix = "http://jayne.hortont.com/web/output/"

if os.uname()[1] == "Kaylee.local":
    www_prefix = "http://localhost/~hortont/output/"

def w(u):
    return www_prefix + u
