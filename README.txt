Diffident
=========

Copyright (C) 2009 by Andy Balaam

http://www.artificialworlds.net/wiki/Diffident

  Diffident is intended to be a diff editor that allows you to adjust
  the files you are comparing. It is also intended to be a patch editor.

Currently, Diffident is a coloured side-by-side diff viewer that works in a terminal.

Usage
-----

To compare two files:

 diffident.py file1 file2

To run the tests:

 diffident.py --test-slow

For full usage information:

 diffident.py --help

Keyboard shortcuts
------------------

                Help - SHIFT-H
                Quit - q
     Move left/right - h/l or Arrow Keys
        Move up/down - k/j or Arrow Keys
 Select line up/down - K/J
       Next/Previous - n/p or F8/F7
        Page up/down - ,/. or PageUp/Down
 Select page up/down - </>
   Scroll left/right - z/x
     Copy left/right - [/]

Code
----

You can find the source code, which is written in Python (making use of the curses module) here: http://github.com/andybalaam/diffident/tree/master

Contact
-------

Andy Balaam <axis3x3@users.sf.net>

