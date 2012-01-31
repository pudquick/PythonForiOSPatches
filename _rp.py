# Currently hosted at HTTP source: http://pastebin.com/raw.php?i=XyMWvV6g

import os as os
import sys as sys

class iPy:
    dir = [x for x in sys.path if ('iPython.app' in x)][0].split('iPython.app')[0]
    documents = dir + 'Documents'
    modules = documents + '/modules'
    scripts = documents + '/User Scripts'

ipython = iPy()

def boot2():
    import os.path, urllib2
    # This will boostrap additional changes
    if (not os.path.exists(ipython.modules)):
        # Make modules path if it doesn't exist
        os.chdir(ipython.documents)
        os.mkdir('modules')
        # Add it to sys.path if not already there
        if not (ipython.modules in sys.path):
            if (not os.path.exists(ipython.modules)):
                sys.path.append(ipython.modules + '')
    # Assuming that this script was downloaded with boostrap.txt, which grabs _scproxy.py, so urllib2 should work
    core_modules = (
        ("_scproxy.py", "http://pastebin.com/raw.php?i=HKnCFcKx"),
        ("_io.py",      "http://pastebin.com/raw.php?i=v9abP7Xt")
        )
    os.chdir(ipython.modules)
    for name,url in core_modules:
        f = urllib2.urlopen(url)
        data = f.read()
        f.close()
        f = open(name, 'wb')
        f.write(data)
        f.close()
        print "Updated: %s (%s)" % (name,url)
        if (os.path.exists(name+'c')):
            os.remove(name+'c')
            print ("* Removed %sc" % name)
    # Cleanup if this is the first time boot2 has been run after bootstrap.txt
    os.chdir(ipython.scripts)
    if (os.path.exists('_scproxy.py')):
        os.remove('_scproxy.py')
        print "* Removed additional _scproxy.py detected in User Scripts."
    if (os.path.exists('_scproxy.pyc')):
        os.remove('_scproxy.pyc')
        print "* Removed _scproxy.pyc detected in User Scripts."
    print "Done. Force quit and re-open, use: from _rp import *"

ipython.boot2 = boot2

import os.path

if not (ipython.modules in sys.path):
    if (os.path.exists(ipython.modules)):
        sys.path.append(ipython.modules + '')
os.chdir(ipython.scripts)
