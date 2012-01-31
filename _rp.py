# Currently hosted at HTTP source: http://pastebin.com/raw.php?i=XyMWvV6g

import os as os
import sys as sys

class iPy:
    dir = [x for x in sys.path if ('iPython.app' in x)][0].split('iPython.app')[0]
    docs = dir + 'Documents'
    mods = docs + '/modules'
    scripts = docs + '/User Scripts'

ipython = iPy()

if not (ipython.mods in sys.path):
    sys.path.append(ipython.mods + '')
os.chdir(ipython.scripts)

