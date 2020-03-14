stolen from https://is.cuni.cz/webapps/zzp/detail/143329/?lang=en by Jakub Břečka. I was unable to find him to ask for permission so we're gonna go with it.

=== REQUIREMENTS ===

0a. OS X 10.10 Yosemite, 10.11 El Capitan or newer.
0b. Xcode 6 or newer (see <http://developer.apple.com>).

1. Brew

	Follow instructions at <http://brew.sh>.

2. Qt

	$ brew install qt5

	Preferred version is 5.5.1.  Check which version you have by:

	$ /usr/local/opt/qt5/bin/qmake -v
	QMake version 3.0
	Using Qt version 5.5.1 in /usr/local/Cellar/qt5/5.5.1_1/lib

3. PyQt5 for Python 2.x:

	$ brew install pyqt5 --with-python --without-python3

3b. Add PyQt5 package into system Python installation.

	$ mkdir -p ~/Library/Python/2.7/lib/python/site-packages
	$ echo 'import site; site.addsitedir("/usr/local/lib/python2.7/site-packages")' >> ~/Library/Python/2.7/lib/python/site-packages/homebrew.pth

4. Install Python packages:

	$ sudo easy_install pip
	$ sudo pip install capstone
	$ sudo pip install distorm3
	$ sudo pip install pycparser

5. Install externally used tools:

	$ brew install graphviz

=== RUNNING ===

Run the IDE with:

	$ ./cricket-gui

=== TESTS ===

Run tests with:

    $ ./cricket-tests

