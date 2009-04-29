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
		FakeDiffLine( "line 15", "line 15", difflinetypes.IDENTICAL ),
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

	actions = [ "l", "n", "n" ]

	assert_strings_equal( view.show( actions ),
"""[d]line 11 [n] * [d]line 11 d
[n]line 12    line 12  
line 13    line 13  
[m]........[n] + [ai]line 14  
[n]line 15    line 15  
                    
                    
""" )

def next_diff_end():

	view = _make_view()

	actions = [ "n", "n", "n", "n", "n" ]

	assert_strings_equal( view.show( actions ),
"""[d]line 11 [n] * [d]line 11 d
[n]line 12    line 12  
line 13    line 13  
[mi]........[n] + [a]line 14  
[n]line 15    line 15  
                    
                    
""" )



def run():
	next_diff_different()
	next_diff_several()
	next_diff_end()

