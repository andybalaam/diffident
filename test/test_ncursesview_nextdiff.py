import curses

from test.asserts import assert_strings_equal

from testlib.fakediffline import FakeDiffLine
from testlib.fakediffmodel import FakeDiffModel

import lib.difflinetypes as difflinetypes
from lib.ncursesview import NCursesView

def _make_view():
	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( "line 01", "line 01", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 02", "line 02", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 03", "line 03", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 04", "line 04", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 05", "line 05", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 06", "line 06", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 07", "line 07", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 08", "line 08", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 09", "line 09", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 10", "line 10 different", difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 11", "line 11 different", difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 12", "line 12", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 13", "line 13", difflinetypes.IDENTICAL ),
		FakeDiffLine( None,      "line 14", difflinetypes.ADD ),
		FakeDiffLine( None,      "line 15", difflinetypes.ADD ),
	]

	view = NCursesView( diffmodel )
	view.win_width = 20
	view.win_height = 7

	return view

def next_diff_different():

	view = _make_view()

	actions = [ "n" ]

	assert_strings_equal( view.show( actions ),
"""[n]line 07    line 07  
line 08    line 08  
line 09    line 09  
[di]line 10 [n] * [d]line 10 d
line 11 [n] * [d]line 11 d
[n]line 12    line 12  
line 13    line 13  
""" )

def next_diff_several():

	view = _make_view()

	actions = [ curses.KEY_RIGHT, "n", "n" ]

	assert_strings_equal( view.show( actions ),
"""[d]line 11 [n] * [d]line 11 d
[n]line 12    line 12  
line 13    line 13  
[m]........[n] + [ai]line 14  
[m]........[n] + [a]line 15  
[n]                    
                    
""" )

def next_diff_end():

	view = _make_view()

	actions = [ "n", "n", "n", "n", "n" ]

	assert_strings_equal( view.show( actions ),
"""[d]line 11 [n] * [d]line 11 d
[n]line 12    line 12  
line 13    line 13  
[mi]........[n] + [a]line 14  
[m]........[n] + [a]line 15  
[n]                    
                    
""" )

def previous_diff():

	view = _make_view()

	actions = [ "n", "n", curses.KEY_DOWN, "p" ]

	assert_strings_equal( view.show( actions ),
"""[n]line 07    line 07  
line 08    line 08  
line 09    line 09  
[di]line 10 [n] * [d]line 10 d
line 11 [n] * [d]line 11 d
[n]line 12    line 12  
line 13    line 13  
""" )

def _make_diff_at_begin_view():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( "line 01", "line 01 different", difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 02", "line 02 different", difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 03", "line 03 different", difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 04", "line 04", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 05", "line 05", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 06", "line 06", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 07", "line 07", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 08", "line 08", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 09", "line 09", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 10", "line 10 different", difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 11", "line 11 different", difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 12", "line 12", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 13", "line 13", difflinetypes.IDENTICAL ),
	]

	view = NCursesView( diffmodel )
	view.win_width = 20
	view.win_height = 3

	return view


def previous_diff_to_beginning():
	"""Track back to the beginning by asking for the previous diff.
	Don't go off to before the beginning."""

	view = _make_diff_at_begin_view()

	actions = [ "n", "n", "p" ]

	assert_strings_equal( view.show( actions ),
"""[di]line 01 [n] * [d]line 01 d
line 02 [n] * [d]line 02 d
line 03 [n] * [d]line 03 d
""" )

def previous_diff_to_beginning_twice():
	"""Track back to the beginning by asking for the previous diff.
	Don't go off to before the beginning."""

	view = _make_diff_at_begin_view()

	actions = [ "n", "n", "p", "p" ]

	assert_strings_equal( view.show( actions ),
"""[di]line 01 [n] * [d]line 01 d
line 02 [n] * [d]line 02 d
line 03 [n] * [d]line 03 d
""" )

def run():
	next_diff_different()
	next_diff_several()
	next_diff_end()
	previous_diff()
	previous_diff_to_beginning()
	previous_diff_to_beginning_twice()

