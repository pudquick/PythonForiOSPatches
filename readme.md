#iPythonPatches - Modules that can be loaded into iPython to enable missing functionality

This repository is a collection of python scripts that function as module replacements for missing builtin modules which weren't included with the distribution of python named "iPython" in the App Store (for iPhone, iPod, and iPad).

##How to use it with your iPython installation:

- Visit this URL in Mobile Safari: https://raw.github.com/pudquick/iPythonPatches/master/bootstrap.txt
- Copy the entire contents (should be able to click and hold to select everything)
- Open up iPython
- Paste the contents into the interpreter (may have to type one letter, then select it, then Paste)
- Press enter

This will download the initial _rp.py and _scproxy.py scripts into your User Scripts folder.

For best results, force quit the iPython app (press Home once to background it, then double-press Home to show a list of recent applications, then press and hold on iPython to reveal a remove icon badge, then remove the iPython icon).

Once installed, usage is a simple single line command in iPython (when starting it):
###from _rp import *


This will get you access to a new 'ipython' object which has the following attributes:

- documents: Path to the iPython.app Documents folder on your device
- scripts: Path to the 'User Scripts' folder in iPython
- modules: Path to a folder called 'modules' in the Documents folder

It also gains you a secondary command you can run:
###boot2()


This command will create the 'modules' directory listed above, if it doesn't exist, move _scproxy.py into it (and out of the User Scripts folder), and additionally download the _io.py module (which allows 'io' to load, giving access to zipfile, gzip, etc.).

Again - for best results, after running boot2, force quit and relaunch iPython.


##Credits

- The modules here are written by pudquick@github 

##License

These modules are released under a standard MIT license.

	Permission is hereby granted, free of charge, to any person
	obtaining a copy of this software and associated documentation files
	(the "Software"), to deal in the Software without restriction,
	including without limitation the rights to use, copy, modify, merge,
	publish, distribute, sublicense, and/or sell copies of the Software,
	and to permit persons to whom the Software is furnished to do so,
	subject to the following conditions:

	The above copyright notice and this permission notice shall be
	included in all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
	EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
	MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
	NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
	BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
	ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
	CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	SOFTWARE.

