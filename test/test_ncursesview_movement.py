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


def run():
	right_arrow()
	right_l()
	left_arrow()
	left_h()
	down_arrow()
	down_j()
	up_arrow()
	up_k()

