Diffident
=========

Copyright (C) 2009 by Andy Balaam

http://www.artificialworlds.net/wiki/Diffident

Diffident is a coloured side-by-side diff viewer and editor that works in a
terminal.

There are also plans to make it possible to edit patch files with Diffident.

Usage
-----

To compare two files:

 diffident file1 file2

To run the tests:

 diffident --test-slow

For full usage information:

 diffident --help

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
         Insert line - a  (Adds a line above the selected line)
      Delete line(s) - d
        Save changes - s  (Saves the file containing the cursor)

Code
----

You can find the source code, which is written in Python (making use of the curses module) here: http://github.com/andybalaam/diffident/tree/master

Contact
-------

Andy Balaam <axis3x3@users.sf.net>

