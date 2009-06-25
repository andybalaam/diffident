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
		DiffLine( "line 2 here", "line 2 here", difflinetypes.IDENTICAL ),
		DiffLine( "line 3 here", "line 3 here", difflinetypes.IDENTICAL ),
		DiffLine( "line 4 here", "line 4 here", difflinetypes.IDENTICAL ),
		DiffLine( "line 5 here", "line 5 here", difflinetypes.IDENTICAL ),
		DiffLine( "line 6 here", "line 6 here", difflinetypes.IDENTICAL ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 2

	return view

def _right( key ):
	view = _make_view()
	actions = [ key ]
	assert_strings_equal( view.show( actions )[0],
"""[n]line 1 here          [ni]line 1 here        
[n]line 2 here          line 2 here        
""" )

def right_arrow():
	_right( curses.KEY_RIGHT )

def right_l():
	_right( "l" )

def right_twice():
	view = _make_view()
	actions = [ curses.KEY_RIGHT, curses.KEY_RIGHT ]
	assert_strings_equal( view.show( actions )[0],
"""[n]line 1 here          [ni]line 1 here        
[n]line 2 here          line 2 here        
""" )



def _left( key ):
	view = _make_view()

	# Go right and then left - back to where we started
	actions = [ curses.KEY_RIGHT, key ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]line 1 here       [n]   line 1 here        
line 2 here          line 2 here        
""" )

def left_arrow():
	_left( curses.KEY_LEFT )

def left_h():
	_left( "h" )

def left_twice():
	view = _make_view()

	actions = [ curses.KEY_LEFT, curses.KEY_LEFT ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]line 1 here       [n]   line 1 here        
line 2 here          line 2 here        
""" )

def _down( key ):
	view = _make_view()

	actions = [ key ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 1 here          line 1 here        
[ni]line 2 here       [n]   line 2 here        
""" )

def down_arrow():
	_down( curses.KEY_DOWN )

def down_j():
	_down( "j" )

def down_twice():
	view = _make_view()

	actions = [ curses.KEY_DOWN, curses.KEY_DOWN, curses.KEY_DOWN,
		curses.KEY_DOWN, curses.KEY_DOWN, curses.KEY_DOWN, curses.KEY_DOWN,
		curses.KEY_DOWN, curses.KEY_DOWN, curses.KEY_DOWN, curses.KEY_DOWN ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 5 here          line 5 here        
[ni]line 6 here       [n]   line 6 here        
""" )

def down_emptyfile():
	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( None, "line 1 here", difflinetypes.ADD ),
		DiffLine( None, "line 2 here", difflinetypes.ADD ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 3

	actions = [ curses.KEY_DOWN, curses.KEY_DOWN, curses.KEY_DOWN,
		curses.KEY_DOWN, curses.KEY_DOWN, curses.KEY_DOWN, curses.KEY_DOWN,
		curses.KEY_DOWN, curses.KEY_DOWN, curses.KEY_DOWN, curses.KEY_DOWN ]

	assert_strings_equal( view.show( actions )[0],
"""[m]..................[ai] + [a]line 1 here        
[mi]..................[ai] + [a]line 2 here        
[n]                                        
""" )


def down_scroll():
	view = _make_view()

	actions = [ curses.KEY_DOWN, curses.KEY_DOWN ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 2 here          line 2 here        
[ni]line 3 here       [n]   line 3 here        
""" )


def _up( key ):
	view = _make_view()

	# Go down and then up - back to where we started
	actions = [ curses.KEY_DOWN, key ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]line 1 here       [n]   line 1 here        
line 2 here          line 2 here        
""" )

def up_arrow():
	_up( curses.KEY_UP )

def up_k():
	_up( "k" )

def up_twice():
	view = _make_view()

	actions = [ curses.KEY_UP, curses.KEY_UP ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]line 1 here       [n]   line 1 here        
line 2 here          line 2 here        
""" )

def up_scroll():
	view = _make_view()

	# Down x 4, Up x 3
	actions = [ curses.KEY_DOWN, curses.KEY_DOWN, curses.KEY_DOWN,
		curses.KEY_DOWN, curses.KEY_UP, curses.KEY_UP, curses.KEY_UP ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]line 2 here       [n]   line 2 here        
line 3 here          line 3 here        
""" )


def _page_down( key ):
	view = _make_view()

	actions = [ key ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]line 3 here       [n]   line 3 here        
line 4 here          line 4 here        
""" )

def page_down_pagedown():
	_page_down( curses.KEY_NPAGE )


def _page_up( key ):
	view = _make_view()

	actions = [ curses.KEY_NPAGE, key ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]line 1 here       [n]   line 1 here        
line 2 here          line 2 here        
""" )

def page_up_pageup():
	_page_up( curses.KEY_PPAGE )


def page_down_cursor_preserved():
	view = _make_view()
	view.win_height = 3

	# Right, Down, PageDown
	actions = [ curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_NPAGE ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 4 here          line 4 here        
line 5 here          [ni]line 5 here        
[n]line 6 here          line 6 here        
""" )

def page_up_cursor_preserved():
	view = _make_view()
	view.win_height = 3

	# Right, Down, PageDown, PageUp
	actions = [ curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_NPAGE,
		curses.KEY_PPAGE ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 1 here          line 1 here        
line 2 here          [ni]line 2 here        
[n]line 3 here          line 3 here        
""" )

def page_down_cursor_to_bottom():
	view = _make_view()
	view.win_height = 3

	# Right, PageDown, PageDown
	actions = [ curses.KEY_RIGHT, curses.KEY_NPAGE,
		curses.KEY_NPAGE ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 4 here          line 4 here        
line 5 here          line 5 here        
line 6 here          [ni]line 6 here        
""" )
	
def page_down_twice():
	view = _make_view()
	view.win_height = 3

	# PageDown, PageDown, PageDown
	actions = [curses.KEY_NPAGE, curses.KEY_NPAGE, curses.KEY_NPAGE ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 4 here          line 4 here        
line 5 here          line 5 here        
[ni]line 6 here       [n]   line 6 here        
""" )


def page_up_cursor_to_top():
	view = _make_view()
	view.win_height = 3

	# Right, Down, PageUp
	actions = [ curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_PPAGE ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 1 here          [ni]line 1 here        
[n]line 2 here          line 2 here        
line 3 here          line 3 here        
""" )

def page_up_twice():
	view = _make_view()
	view.win_height = 3

	# PageUp, PageUp
	actions = [ curses.KEY_PPAGE, curses.KEY_PPAGE ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]line 1 here       [n]   line 1 here        
line 2 here          line 2 here        
line 3 here          line 3 here        
""" )

def _make_wide_view():
	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( "0-23456789abcdef", "0-23456789abcdef", difflinetypes.IDENTICAL ),
		DiffLine( "1-23456789abcdef", "1-23456789abcdef plus extr",
			difflinetypes.DIFFERENT ),
		DiffLine( None, "2-23456789abcdef plus extr", difflinetypes.ADD ),
		DiffLine( "3-23456789abcdef", None, difflinetypes.REMOVE ),
		DiffLine( "4-23456789abcdef", "4-23456789abcdef", difflinetypes.IDENTICAL ),
		DiffLine( "5-23456789abcdef", "5-23456789abcdef plus ext", difflinetypes.DIFFERENT ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 23
	view.win_height = 2

	return view


def page_right():
	view = _make_wide_view()

	# PageRight
	actions = [ "x" ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]56789abcde[n]   56789abcde
[d]56789abcde[di] * [d]56789abcde
""" )

def page_right_thrice():
	view = _make_wide_view()

	# PageRight 3 times
	actions = [ "x", "x", "x" ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]f         [n]   f         
[d]f         [di] * [d]f plus ext
""" )

def page_right_stop_at_end():
	view = _make_wide_view()

	# PageRight many times - we should stop before
	# it's just an empty screen
	actions = [ "x", "x", "x", "x", "x", "x", "x", "x" ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]          [n]             
[d]          [di] * [d]r         
""" )

def page_left():
	view = _make_wide_view()

	# PageRight, PageLeft
	actions = [ "x", "z" ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]0-23456789[n]   0-23456789
[d]1-23456789[di] * [d]1-23456789
""" )

def page_left_stop_at_beginning():
	view = _make_wide_view()

	# PageRight, PageLeft 3 times
	actions = [ "x", "z", "z", "z" ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]0-23456789[n]   0-23456789
[d]1-23456789[di] * [d]1-23456789
""" )

def page_right_page_down():
	view = _make_wide_view()

	# Right, Down, PageRight, PageDown
	actions = [ curses.KEY_RIGHT, curses.KEY_DOWN,
		"x", curses.KEY_NPAGE ]

	assert_strings_equal( view.show( actions )[0],
"""[m]..........[ai] + [a]56789abcde
[r]56789abcde[ri] - [mi]..........
""" )

def page_right_page_down_shorter_lines():
	view = _make_wide_view()

	# PageRight 5 times, PageDown twice - should jump back to
	# a scroll position with some visible characters
	actions = [ "x", "x", "x", "x", "x", curses.KEY_NPAGE,
		curses.KEY_NPAGE ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]          [n]             
[d]          [di] * [d]s ext     
""" )

def _make_short_diff_view():
	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( "line 01", "line 01", difflinetypes.IDENTICAL ),
		DiffLine( "line 02", "line 02", difflinetypes.IDENTICAL ),
	]

	view = NCursesView( diffmodel )
	view.win_width = 20
	view.win_height = 4

	return view

def page_down_short_diff():
	view = _make_short_diff_view()
	actions = [ curses.KEY_NPAGE ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 01    line 01  
[ni]line 02 [n]   line 02  
                    
                    
""" )

def page_down_twice_short_diff():
	view = _make_short_diff_view()
	actions = [ curses.KEY_NPAGE, curses.KEY_NPAGE ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 01    line 01  
[ni]line 02 [n]   line 02  
                    
                    
""" )

def page_up_short_diff():
	view = _make_short_diff_view()
	actions = [ curses.KEY_PPAGE ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]line 01 [n]   line 01  
line 02    line 02  
                    
                    
""" )


def run():
	right_arrow()
	right_l()
	right_twice()
	left_arrow()
	left_h()
	left_twice()
	down_arrow()
	down_j()
	down_twice()
	down_scroll()
	down_emptyfile()
	up_arrow()
	up_k()
	up_twice()
	up_scroll()

	page_down_pagedown()
	page_down_cursor_preserved()
	page_down_cursor_to_bottom()
	page_down_twice()
	page_up_pageup()
	page_up_cursor_preserved()
	page_up_cursor_to_top()
	page_up_twice()
	page_down_short_diff()
	page_down_twice_short_diff()
	page_up_short_diff()

	page_right()
	page_right_thrice()
	page_right_stop_at_end()
	page_left()
	page_left_stop_at_beginning()
	page_right_page_down()
	page_right_page_down_shorter_lines()

