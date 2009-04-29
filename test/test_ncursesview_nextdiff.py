import curses

from test.asserts import assert_strings_equal

from testlib.fakediffline import FakeDiffLine
from testlib.fakediffmodel import FakeDiffModel

import lib.difflinetypes as difflinetypes
from lib.ncursesview import NCursesView

def next_diff_different():
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
		FakeDiffLine( "line 11", "line 11", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 12", "line 12", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 13", "line 13", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 14", "line 14", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 15", "line 15", difflinetypes.IDENTICAL ),
	]

	view = NCursesView( diffmodel )
	view.win_width = 20
	view.win_height = 7

	actions = [ "n" ]

	assert_strings_equal( view.show( actions ),
"""[n]line 07    line 07  
line 08    line 08  
line 09    line 09  
[di]line 10 [n] * [d]line 10 d
[n]line 11    line 11  
line 12    line 12  
line 13    line 13  
""" )


def run():
	next_diff_different()

