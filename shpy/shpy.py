import sys, os, os.path, zipfile, tarfile, shutil, urllib2, xmlrpclib

class _Shpy:
    def split_leading_dir(self, path):
        path = str(path)
        path = path.lstrip('/').lstrip('\\')
        if '/' in path and (('\\' in path and path.find('/') < path.find('\\'))
                            or '\\' not in path):
            return path.split('/', 1)
        elif '\\' in path:
            return path.split('\\', 1)
        else:
            return path, ''

    def has_leading_dir(self, paths):
        common_prefix = None
        for path in paths:
            prefix, rest = self.split_leading_dir(path)
            if not prefix:
                return False
            elif common_prefix is None:
                common_prefix = prefix
            elif prefix != common_prefix:
                return False
        return True

    def sizeof_fmt(self, num):
        for x in ['bytes','KB','MB','GB']:
            if num < 1024.0:
                if (x == 'bytes'):
                    return "%s %s" % (num, x)
                else:
                    return "%3.1f %s" % (num, x)
            num /= 1024.0
        return "%3.1f%s" % (num, 'TB')

    def f_help(self, argv):
        print self.hmsg

    def f_ls(self, argv):
        files = argv[1:]
        if (not files):
            files = ['.']
        files_for_path = dict()
        for file in files:
            full_file = os.path.abspath(file).rstrip('/')
            file_name = os.path.basename(full_file)
            dir_name  = os.path.dirname(full_file).rstrip('/')
            if (not os.path.exists(full_file)):
                print "! Error: Skipped, missing -", self.pretty_path(file)
                continue
            if (os.path.isdir(full_file)):
                # Need to add this as a key and all the files contained inside it
                _dirs = files_for_path.get(full_file, set())
                for new_file in os.listdir(full_file):
                    _dirs.add(full_file.rstrip('/') + '/' + new_file.rstrip('/'))
                files_for_path[full_file] = _dirs
            else:
                _dirs = files_for_path.get(dir_name, set())
                _dirs.add(full_file)
                files_for_path[dir_name] = _dirs
        # Iterate over the paths, in alphabetical order:
        paths = sorted(files_for_path.keys())
        cwd = os.getcwd().rstrip('/')
        in_cwd = False
        if (cwd in paths):
            # Move cwd to the front, mark that it's present
            paths.remove(cwd)
            paths = [cwd] + paths
            in_cwd = True
        for i,path in enumerate(paths):
            if (i > 0):
                print "\n" + self.pretty_path(path) + "/:"
            elif (not in_cwd):
                print self.pretty_path(path) + "/:"
            for file in sorted(list(files_for_path[path])):
                full_file = os.path.abspath(file).rstrip('/')
                file_name = os.path.basename(full_file)
                if (os.path.isdir(full_file)):
                    print file_name + "/"
                else:
                    print file_name + (" (%s)" % (self.sizeof_fmt(os.stat(full_file).st_size)))

    def f_cd(self, argv):
        target = (argv[1:2] or ['/'])[0]
        try:
            print "* Changing path to:", self.pretty_path(target)
            os.chdir(target)
            print "* Path is now:", self.pretty_path(os.getcwd())
        except:
            print "! Error:", sys.exc_info()[1]
            print "* Path is now:", self.pretty_path(os.getcwd())

    def f_mkdir(self, argv):
        if (len(argv) != 2):
            print "* Usage: mkdir dirname"
            return 0
        target = argv[1]
        if os.path.exists(target):
            print "! Error: Exists -", self.pretty_path(os.path.abspath(target))
            return 0
        try:
            print "* Creating dir:", self.pretty_path(target)
            os.mkdir(target)
            print "* Made at:", self.pretty_path(os.path.abspath(target))
        except:
            print "! Error:", sys.exc_info()[1]

    def f_cat(self, argv):
        if (len(argv) != 2):
            print "* Usage: cat file"
            return 0
        target = argv[1]
        if (not os.path.exists(target)):
            print "! Error: Not found -", self.pretty_path(os.path.abspath(target))
            return 0
        if (os.path.isdir(target)):
            print "! Error: Target is a directory."
            return 0
        try:
            f = open(target)
            contents = f.read()
            f.close()
            print contents
            print ""
        except:
            print "! Error:", sys.exc_info()[1]

    def f_rm(self, argv):
        if (len(argv) < 2):
            print "* Usage: rm file [..]"
            return 0
        for file in argv[1:]:
            full_file = os.path.abspath(file).rstrip('/')
            if not os.path.exists(file):
                print "! Error: Not found -", self.pretty_path(file)
                continue
            if (full_file.lower() == os.getcwd().rstrip('/').lower()):
                print "! Error: Skipped rm of current dir (.)"
                continue
            if (os.path.isdir(full_file)):
                try:
                    shutil.rmtree(full_file, True)
                    if (os.path.exists(full_file)):
                        print "! Error: Could not rm -", self.pretty_path(file)
                    else:
                        print "* rm'd:", self.pretty_path(full_file)
                except:
                    print "! Error:", sys.exc_info()[1]                
            else:
                try:
                    os.remove(full_file)
                    print "* rm'd:", self.pretty_path(full_file)
                except:
                    print "! Error:", sys.exc_info()[1]

    def f_cp(self, argv):
        if (not (len(argv) >= 3)):
            print "* Usage: cp src [..] dest"
            return 0
        dest  = argv[-1]
        files = argv[1:-1]
        if (len(files) > 1):
            # Copying multiple files, destination must be an existing directory.
            if (not os.path.isdir(dest)):
                print "! Error: No such dir -", self.pretty_path(os.path.abspath(dest))
                return 0
            full_dest = os.path.abspath(dest).rstrip('/') + '/'
            did_copy = False
            for file in files:
                full_file = os.path.abspath(file).rstrip('/')
                file_name = os.path.basename(full_file)
                new_name  = full_dest + file_name
                if (not os.path.exists(full_file)):
                    print "! Error: Skipped, missing -", self.pretty_path(file)
                    continue
                if (full_file.lower() == os.getcwd().rstrip('/').lower()):
                    print "! Error: Skipped cp of current dir (.)"
                    continue
                try:
                    if (os.path.isdir(full_file)):
                        shutil.copytree(full_file,new_name)
                    else:
                        shutil.copy(full_file,new_name)
                    print "* cp'd:", self.pretty_path(full_file)
                    did_copy = True
                except:
                    "! Error:", sys.exc_info()[1]
            if (did_copy):
                print "* ..to:", self.pretty_path(full_dest)
        else:
            # Copying a single file to a (pre-existing) directory or a file
            file = files[0]
            full_file = os.path.abspath(file).rstrip('/')
            file_name = os.path.basename(full_file)
            full_dest = os.path.abspath(dest).rstrip('/')
            if (os.path.isdir(full_dest)):
                if (os.path.exists(full_file)):
                    try:
                        shutil.copytree(full_file,full_dest + '/' + file_name)
                        print "* cp'd:", self.pretty_path(full_file)
                        print "* ..to:", self.pretty_path(full_dest + '/' + file_name)
                    except:
                        print "! Error:", sys.exc_info()[1]
                else:
                    print "! Error: No such file -", self.pretty_path(file)
                    return 0
            else:
                if (os.path.exists(full_file)):
                    try:
                        shutil.copy(full_file,full_dest)
                        print "* cp'd:", self.pretty_path(full_file)
                        print "* ..to:", self.pretty_path(full_dest)
                    except:
                        print "! Error:", sys.exc_info()[1]
                else:
                    print "! Error: No such file -", self.pretty_path(file)
                    return 0

    def f_mv(self, argv):
        if (not (len(argv) >= 3)):
            print "* Usage: mv src [..] dest"
            return 0
        dest  = argv[-1]
        files = argv[1:-1]
        if (len(files) > 1):
            # Moving multiple files, destination must be an existing directory.
            if (not os.path.isdir(dest)):
                print "! Error: No such dir -", self.pretty_path(os.path.abspath(dest))
                return 0
            full_dest = os.path.abspath(dest).rstrip('/') + '/'
            did_move = False
            for file in files:
                full_file = os.path.abspath(file).rstrip('/')
                file_name = os.path.basename(full_file)
                new_name  = full_dest + file_name
                if (not os.path.exists(full_file)):
                    print "! Error: Skipped, missing -", self.pretty_path(file)
                    continue
                if (full_file.lower() == os.getcwd().rstrip('/').lower()):
                    print "! Error: Skipped mv of current dir (.)"
                    continue
                try:
                    os.rename(full_file,new_name)
                    print "* mv'd:", self.pretty_path(full_file)
                    did_move = True
                except:
                    "! Error:", sys.exc_info()[1]
            if (did_move):
                print "* ..to:", self.pretty_path(full_dest)
        else:
            # Moving a single file to a (pre-existing) directory or a file
            file = files[0]
            full_file = os.path.abspath(file).rstrip('/')
            file_name = os.path.basename(full_file)
            full_dest = os.path.abspath(dest).rstrip('/')
            if (os.path.isdir(full_dest)):
                if (os.path.exists(full_file)):
                    try:
                        os.rename(full_file, full_dest + '/' + file_name)
                        print "* mv'd:", self.pretty_path(full_file)
                        print "* ..to:", self.pretty_path(full_dest + '/' + file_name)
                    except:
                        print "! Error:", sys.exc_info()[1]
                else:
                    print "! Error: No such file -", self.pretty_path(file)
                    return 0
            else:
                if (os.path.exists(full_file)):
                    try:
                        os.rename(full_file, full_dest)
                        print "* mv'd:", self.pretty_path(full_file)
                        print "* ..to:", self.pretty_path(full_dest)
                    except:
                        print "! Error:", sys.exc_info()[1]
                else:
                    print "! Error: No such file -", self.pretty_path(file)
                    return 0

    def f_pwd(self, argv):
            print self.pretty_path(os.getcwd())

    def chunk_report(self, bytes_so_far, chunk_size, total_size):
        if (total_size != None):
            percent = float(bytes_so_far) / total_size
            percent = round(percent*100, 2)
            print "Downloaded %d of %d bytes (%0.2f%%)" % (bytes_so_far, total_size, percent)
            if bytes_so_far >= total_size:
                print ""
        else:
            print "Downloaded %d bytes" % (bytes_so_far)

    def chunk_read(self, response, chunk_size=8192, report_hook=None, filename=None):
        file_data = []
        if response.info().has_key('Content-Length'):
            total_size = response.info().getheader('Content-Length').strip()
            total_size = int(total_size)
        else:
            # No size
            total_size = None
            print "* Warning: No total file size available."
        if (filename == None) and (response.info().has_key('Content-Disposition')):
            # If the response has Content-Disposition, we take file name from it
            try:
                filename = response.info()['Content-Disposition'].split('filename=')[1]
                if filename[0] == '"' or filename[0] == "'":
                    filename = filename[1:-1]
            except:
                filename = "output"     
        if (filename == None):
            print "* No detected filename, using 'output'"
            filename = "output"
        bytes_so_far = 0
        while True:
            chunk = response.read(chunk_size)
            bytes_so_far += len(chunk)
            if not chunk:
                break
            else:
                file_data.append(chunk)
            report_hook(bytes_so_far, chunk_size, total_size)
        return (file_data, filename)


    def f_get(self, argv):
        if (not (2 <= len(argv) <= 3)):
            print "* Usage: get URL [file]"
            return 0
        target = argv[1]
        output = (argv[2:] or [None])[0]
        if (not (target.lower().startswith('http://') or target.lower().startswith('https://'))):
            print "* Error: URL must start with http:// or https://"
            return 0
        headers = {'User-Agent' : "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6;en-US; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9"}
        req = urllib2.Request(target, headers=headers)
        print "* Downloading:", target
        response = urllib2.urlopen(req)
        if (output == None):
            try:
                output = target.split('/')[-1].split('#')[0].split('?')[0]
            finally:
                if (not output):
                    output = None
        data,filename = self.chunk_read(response, report_hook=self.chunk_report, filename=output)
        if (len(data) > 0):
            try:
                f = open(filename, "wb")
                for x in data:
                    f.write(x)
                f.close()
                print "* Saved to:", self.pretty_path(filename)
            except:
                print "! Error:", sys.exc_info()[1]
        else:
            print "* Error: 0 bytes downloaded, not saved"

    def f_exit(self, argv):
        print "*** Exiting shpy ***"
        return 1

    def f_pypi_search(self, argv):
        if (not (len(argv) >= 2)):
            print "* Usage: pypi-search <package name>"
            return 0
        pkg_name = ' '.join(argv[1:])
        pypi = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
        hits = pypi.search({'name': pkg_name}, 'and')
        if (not hits):
            print "* PyPI: No matches found."
            return 0
        print "* Found %s match%s:" % (len(hits), ((len(hits) > 1) and 'es') or '')
        for p in sorted(hits, key=lambda pkg: pkg['_pypi_ordering'], reverse=True):
            print "  %s:" % (p['name'])
            print '   "%s"' % (p['summary'])

    def f_pypi_vers(self, argv):
        if (not (len(argv) >= 2)):
            print "* Usage: pypi-search <package name>"
            return 0
        pkg_name = ' '.join(argv[1:])
        pypi = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
        hits = pypi.package_releases(pkg_name, True)
        if (not hits):
            print "* PyPI: None available for:", pkg_name
            return 0
        print "* Available version%s:" % (((len(hits) > 1) and 's') or '')
        print ', '.join(hits)

    def f_unzip(self, argv):
        # filename, location
        if (not (2 <= len(argv) <= 3)):
            print "* Usage: unzip file.zip [destdir]"
            return 0
        filename = os.path.abspath(argv[1])
        if (not filename.lower().endswith('.zip')):
            print "! Error: Needs a .zip name -", self.pretty_path(argv[1])
            return 0
        location = (argv[2:3] or [os.path.dirname(filename) + "/" + os.path.splitext(os.path.basename(filename))[0]])[0]
        if not os.path.exists(filename):
            print "! Error: No such file -", self.pretty_path(argv[1])
            return 0
        if not os.path.exists(location):
            os.makedirs(location)
        zipfp = open(filename, 'rb')
        try:
            print "* Unzipping:", self.pretty_path(filename)
            print "* To path:",  self.pretty_path(os.path.abspath(location))
            zip = zipfile.ZipFile(zipfp)
            leading = self.has_leading_dir(zip.namelist())
            for name in zip.namelist():
                data = zip.read(name)
                fn = name
                if leading:
                    fn = self.split_leading_dir(name)[1]
                fn = os.path.join(location, fn)
                dir = os.path.dirname(fn)
                if not os.path.exists(dir):
                    os.makedirs(dir)
                if fn.endswith('/') or fn.endswith('\\'):
                    # A directory
                    if not os.path.exists(fn):
                        os.makedirs(fn)
                else:
                    fp = open(fn, 'wb')
                    try:
                        fp.write(data)
                    finally:
                        fp.close()
        except:
            zipfp.close()
            print "! Error: Bad .zip / problem unzipping"
            return 0
        finally:
            zipfp.close()

    def f_untar(self, argv):
        # filename, location
        if (not (2 <= len(argv) <= 3)):
            print "* Usage: untar file.tar [destdir]"
            return 0
        filename = os.path.abspath(argv[1])
        if (not (filename.lower().endswith('.tar') or filename.lower().endswith('.tgz') or filename.lower().endswith('.tar.gz'))):
            print "! Error: Needs a .tar/.tar.gz/.tgz name -", self.pretty_path(argv[1])
            return 0
        elif filename.lower().endswith('.tar.gz'):
            base_filename = os.path.basename(filename)[:-7]
        else:
            base_filename = os.path.splitext(os.path.basename(filename))[0]
        location = (argv[2:3] or [os.path.dirname(filename) + "/" + base_filename])[0]
        if not os.path.exists(location):
            os.makedirs(location)
        if filename.lower().endswith('.gz') or filename.lower().endswith('.tgz'):
            mode = 'r:gz'
        else:
            mode = 'r'
        tar = tarfile.open(filename, mode)
        try:
            leading = self.has_leading_dir([member.name for member in tar.getmembers() if member.name != 'pax_global_header'])
            print "* Untarring:", self.pretty_path(filename)
            print "* To path:",  self.pretty_path(os.path.abspath(location))
            for member in tar.getmembers():
                fn = member.name
                if fn == 'pax_global_header':
                    continue
                if leading:
                    fn = self.split_leading_dir(fn)[1]
                path = os.path.join(location, fn)
                if member.isdir():
                    if not os.path.exists(path):
                        os.makedirs(path)
                elif member.issym():
                    # skip symlinks
                    print "! Skipped symlink -", member.name
                    continue
                else:
                    try:
                        fp = tar.extractfile(member)
                    except (KeyError, AttributeError):
                        e = sys.exc_info()[1]
                        print "! Error: Invalid -", member.name, ":", e
                        continue
                    if not os.path.exists(os.path.dirname(path)):
                        os.makedirs(os.path.dirname(path))
                    destfp = open(path, 'wb')
                    try:
                        shutil.copyfileobj(fp, destfp)
                    finally:
                        destfp.close()
                    fp.close()
        finally:
            tar.close()

    def f_selfupdate(self, argv):
        self.f_get(['get', 'https://raw.github.com/pudquick/PythonForiOSPatches/master/shpy/shpy.py'])

    def f_vars(self, argv):
        for k in sorted(self.bp.env_vars.keys()):
            print "%s: %s" % (k, self.bp.env_vars[k])

    def f_error(self, argv):
        if (argv[:1]):
            print "! Unknown cmd: %s - try: help" % argv[0]
        else:
            print "! Unknown cmd - try: help"

    def __init__(self):
        # Hiding away BashParser from a wildcard import of shpy
        # Let's keep those globals tidy!
        from bash_alike import BashParser
        self.available_cmds = {"quit":   self.f_exit,
                               "logout": self.f_exit,
                               "exit":   self.f_exit,
                               "help":   self.f_help,
                               "h":      self.f_help,
                               "?":      self.f_help,
                               "cd":     self.f_cd,
                               "pwd":    self.f_pwd,
                               "mv":     self.f_mv,
                               "cp":     self.f_cp,
                               "rm":     self.f_rm,
                               "ls":     self.f_ls,
                               "dir":    self.f_ls,
                               "cat":    self.f_cat,
                               "get":    self.f_get,
                               "curl":   self.f_get,
                               "wget":   self.f_get,
                               "mkdir":  self.f_mkdir,
                               "untar":  self.f_untar,
                               "unzip":  self.f_unzip,
                               "vars":   self.f_vars,
                               "pypi-search": self.f_pypi_search,
                               "pypi-vers":   self.f_pypi_vers,
                               "selfupdate":  self.f_selfupdate}
        self.hmsg = "Available commands:\n"                    + \
                    "-------------------\n"                    + \
                    "help - Shows help (also: h, ?)\n"         + \
                    "exit - Quits shpy (also: logout, quit)\n" + \
                    "pwd       - Show current directory\n"     + \
                    "ls [file ..] - List file(s)\n"            + \
                    "cd [dir]  - Change directory\n"           + \
                    "mkdir dir - Create directory\n"           + \
                    "cat file - Print file to screen\n"        + \
                    "unzip file.zip [destdir] - Unzip file\n"  + \
                    "untar file.tar [destdir] - Untar file\n"  + \
                    "rm file [..] - Delete files and dirs\n"   + \
                    "mv src [..] dest - Move file(s)\n"        + \
                    "cp src [..] dest - Copy file(s)\n"        + \
                    "get URL [file] - Download file\n"         + \
                    "selfupdate - Update shpy\n"               + \
                    "vars - List variables and values"
        self.bp = BashParser()
        try:
            dir = [x for x in sys.path if ('Python for iOS.app' in x)][0].split('Python for iOS.app')[0]
            if (dir.startswith('/var')):
                dir = '/private' + dir
        except:
            dir = '/'
        documents = dir + 'Documents'
        modules = documents + '/Modules'
        scripts = documents + '/User Scripts'
        if (os.getcwd() == '/'):
            # Chances are we're being run without _rp
            os.chdir(scripts)
        env_vars = {'$HOME': documents,
                    '$SCRIPTS': scripts,
                    '$MODULES': modules}
        self.bp.env_vars = env_vars

    def pretty_path(self, path_string):
        base = self.bp.env_vars['$HOME'].rstrip('/')
        if ((base == '') or (not path_string.startswith(base))):
            return path_string
        fixed = path_string[len(base):]
        if (fixed):
            return '~' + fixed
        return '~/'

    def parse_cmd(self, argv):
        cmd = (argv[:1] or [None])[0]
        return (self.available_cmds.get(cmd, self.f_error))(argv)

    def fixed_raw_input(self, prompt):
        # Temporary workaround for ongoing bug in Python for iOS
        sys.stdout.write(prompt)
        sys.stdout.flush()
        return raw_input().rstrip('\r\n')

    def main_loop(self):
        while True:
            command_str = self.fixed_raw_input('$> ')
            try:
                command_list = self.bp.bash_parse(command_str)
                if (command_list):
                    if (self.parse_cmd(command_list)):
                        return
            except SyntaxError, msg:
                print "*** Error:", msg
            except:
                print "*** Error:", sys.exc_info()[1]
                return

# More hiding here, whee
_shpy = _Shpy()
shpy  = _shpy.main_loop
