import curses

from test.asserts import assert_strings_equal

from testlib.fakediffline import FakeDiffLine
from testlib.fakediffmodel import FakeDiffModel

import lib.difflinetypes as difflinetypes
from lib.ncursesview import NCursesView

def _make_view():
	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( "line 1 here", "line 1 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 2 here", "line 2 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 3 here", "line 3 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 4 here", "line 4 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 5 here", "line 5 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 6 here", "line 6 here", difflinetypes.IDENTICAL ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 2

	return view

def _right( key ):
	view = _make_view()
	actions = [ key ]
	assert_strings_equal( view.show( actions ),
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
	assert_strings_equal( view.show( actions ),
"""[n]line 1 here          [ni]line 1 here        
[n]line 2 here          line 2 here        
""" )



def _left( key ):
	view = _make_view()

	# Go right and then left - back to where we started
	actions = [ curses.KEY_RIGHT, key ]

	assert_strings_equal( view.show( actions ),
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

	assert_strings_equal( view.show( actions ),
"""[ni]line 1 here       [n]   line 1 here        
line 2 here          line 2 here        
""" )

def _down( key ):
	view = _make_view()

	actions = [ key ]

	assert_strings_equal( view.show( actions ),
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

	assert_strings_equal( view.show( actions ),
"""[n]line 5 here          line 5 here        
[ni]line 6 here       [n]   line 6 here        
""" )

def down_scroll():
	view = _make_view()

	actions = [ curses.KEY_DOWN, curses.KEY_DOWN ]

	assert_strings_equal( view.show( actions ),
"""[n]line 2 here          line 2 here        
[ni]line 3 here       [n]   line 3 here        
""" )


def _up( key ):
	view = _make_view()

	# Go down and then up - back to where we started
	actions = [ curses.KEY_DOWN, key ]

	assert_strings_equal( view.show( actions ),
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

	assert_strings_equal( view.show( actions ),
"""[ni]line 1 here       [n]   line 1 here        
line 2 here          line 2 here        
""" )

def up_scroll():
	view = _make_view()

	# Down x 4, Up x 3
	actions = [ curses.KEY_DOWN, curses.KEY_DOWN, curses.KEY_DOWN,
		curses.KEY_DOWN, curses.KEY_UP, curses.KEY_UP, curses.KEY_UP ]

	assert_strings_equal( view.show( actions ),
"""[ni]line 2 here       [n]   line 2 here        
line 3 here          line 3 here        
""" )


def _page_down( key ):
	view = _make_view()

	actions = [ key ]

	assert_strings_equal( view.show( actions ),
"""[ni]line 3 here       [n]   line 3 here        
line 4 here          line 4 here        
""" )

def page_down_pagedown():
	_page_down( curses.KEY_NPAGE )


def _page_up( key ):
	view = _make_view()

	actions = [ curses.KEY_NPAGE, key ]

	assert_strings_equal( view.show( actions ),
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

	assert_strings_equal( view.show( actions ),
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

	assert_strings_equal( view.show( actions ),
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

	assert_strings_equal( view.show( actions ),
"""[n]line 4 here          line 4 here        
line 5 here          line 5 here        
line 6 here          [ni]line 6 here        
""" )
	
def page_down_twice():
	view = _make_view()
	view.win_height = 3

	# PageDown, PageDown, PageDown
	actions = [curses.KEY_NPAGE, curses.KEY_NPAGE, curses.KEY_NPAGE ]

	assert_strings_equal( view.show( actions ),
"""[n]line 4 here          line 4 here        
line 5 here          line 5 here        
[ni]line 6 here       [n]   line 6 here        
""" )


def page_up_cursor_to_top():
	view = _make_view()
	view.win_height = 3

	# Right, Down, PageUp
	actions = [ curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_PPAGE ]

	assert_strings_equal( view.show( actions ),
"""[n]line 1 here          [ni]line 1 here        
[n]line 2 here          line 2 here        
line 3 here          line 3 here        
""" )

def page_up_twice():
	view = _make_view()
	view.win_height = 3

	# PageUp, PageUp
	actions = [ curses.KEY_PPAGE, curses.KEY_PPAGE ]

	assert_strings_equal( view.show( actions ),
"""[ni]line 1 here       [n]   line 1 here        
line 2 here          line 2 here        
line 3 here          line 3 here        
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

