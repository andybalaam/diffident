#   Diffident, an interactive diff viewer and editor
#   Copyright (C) 2009 Andy Balaam <axis3x3@users.sf.net>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import curses

from test.asserts import assert_strings_equal

from lib.diffmodels.diffline import DiffLine
from testlib.fakediffmodel import FakeDiffModel

from lib.misc.constants import difflinetypes
from lib.views.ncursesview import NCursesView

def _make_view():
	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( "line 1 here", "line 1 here", difflinetypes.IDENTICAL ),
	]

	view = NCursesView( diffmodel )
	view.win_width  = 80
	view.win_height = 20

	return view

def normal():
	view = _make_view()
	actions = [ "H" ]

	assert_strings_equal( view.show( actions )[0],
"""[n]                                                                                
                                 Diffident Help                                 
                                                                                
                                    Quit - q                                    
                         Move left/right - h/l or Arrow Keys                    
                            Move up/down - k/j or Arrow Keys                    
                     Select line up/down - K/J                                  
                Next/Previous difference - n/p or F8/F7                         
                            Page up/down - ,/. or PageUp/Down                   
                     Select page up/down - </>                                  
                       Scroll left/right - z/x                                  
                         Copy left/right - [/]                                  
                          Delete line(s) - d                                    
                            Save changes - s                                    
                                                                                
                                                                                
   Diffident is Copyright (C) 2009 Andy Balaam and the Diffident developers.    
                  Diffident comes with ABSOLUTELY NO WARRANTY.                  
  This is free software, and you are welcome to redistribute it under certain   
 conditions; see the file COPYING for details, or gnu.org/licenses/gpl-2.0.txt  
""" )

def run():
	normal()
