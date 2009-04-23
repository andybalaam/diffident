import curses

from test.asserts import assert_strings_equal

from testlib.fakediffline import FakeDiffLine
from testlib.fakediffmodel import FakeDiffModel

import lib.difflinetypes as difflinetypes
from lib.ncursesview import NCursesView

def pad_to_width():
	diffmodel = FakeDiffModel()
	view = NCursesView( diffmodel )

	assert_strings_equal( view.pad_to_width( None, 5 ), "     " )
	assert_strings_equal( view.pad_to_width( "d f", 5 ), "d f  " )
	assert_strings_equal( view.pad_to_width( "d fffffffff", 5 ), "d fffffffff" )

def _right( key ):

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( "line 1 here", "line 1 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 2 here", "line 2 here", difflinetypes.IDENTICAL ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 2

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

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( "line 1 here", "line 1 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 2 here", "line 2 here", difflinetypes.IDENTICAL ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 2

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


def run():
	right_arrow()
	right_l()
	left_arrow()
	left_h()

