#PythonForiOSPatches - Modules that can be loaded into "Python for iOS" (available in the iOS App Store) to enable missing functionality

This repository is a collection of python scripts that function as module replacements for missing builtin modules which weren't included with the distribution of python named "iPython" in the App Store (for iPhone, iPod, and iPad).

Thank you, Jonathan Hosmer, for bringing python to my iPhone! You are the one reason I'm not jailbreaking my device.

I'm happy I could play some small part in making it work even better in iOS :)

##How to use it:

- This section of the documentation will be updated to reflect usage of any new scripts I add. The original documentation here was for version 1.1 and has been archived in the folder containing the 1.1 code.

However, there is one thing currently available in 1.2 which was part of my 1.1 scripts which is currently not documented in Python for iOS:
```python
from _rp import pythonforios
```

This will get you access to a new 'pythonforios' object which has the following attributes:

- documents: Path to the app's Documents folder on your device
- scripts: Path to the 'User Scripts' folder
- modules: Path to a folder called 'modules' in the Documents folder


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

