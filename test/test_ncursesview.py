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

def same():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( "line 1 here", "line 1 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 2 here", "line 2 here", difflinetypes.IDENTICAL ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 5

	actions = []

	assert_strings_equal( view.show( actions ),
"""[ni]line 1 here       [n]   line 1 here        
line 2 here          line 2 here        
                                        
                                        
                                        
""" )


def differences():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( "line 1 here", "line 1 here different",
			difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 2 here", "line 2 here different",
			difflinetypes.DIFFERENT ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 5

	actions = []

	assert_strings_equal( view.show( actions ),
"""[di]line 1 here       [n] * [d]line 1 here differe
line 2 here       [n] * [d]line 2 here differe
[n]                                        
                                        
                                        
""" )

def adds():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( None, "line 1 here",
			difflinetypes.ADD ),
		FakeDiffLine( None, "line 2 here",
			difflinetypes.ADD ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 5

	actions = []

	assert_strings_equal( view.show( actions ),
"""[mi]                  [n] + [a]line 1 here        
[m]                  [n] + [a]line 2 here        
[n]                                        
                                        
                                        
""" )

def removes():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( "line 1 here", None,
			difflinetypes.REMOVE ),
		FakeDiffLine( "line 2 here", None,
			difflinetypes.REMOVE ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 39
	view.win_height = 5

	actions = []

	assert_strings_equal( view.show( actions ),
"""[ri]line 1 here       [n] - [m]                  
[r]line 2 here       [n] - [m]                  
[n]                                       
                                       
                                       
""" )




def mixture():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( "line 1 here", "line 1 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( None, "line 2 here",
			difflinetypes.ADD ),
		FakeDiffLine( "line 3 here", "line 3 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 4 here", "line 4 here different",
			difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 5 here", None,
			difflinetypes.REMOVE ),
		FakeDiffLine( "line 6 here", "line 6 here", difflinetypes.IDENTICAL ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 5

	actions = []

	assert_strings_equal( view.show( actions ),
"""[ni]line 1 here       [n]   line 1 here        
[m]                  [n] + [a]line 2 here        
[n]line 3 here          line 3 here        
[d]line 4 here       [n] * [d]line 4 here differe
[r]line 5 here       [n] - [m]                   
""" )

def run():
	pad_to_width()
	same()
	differences()
	adds()
	removes()
	mixture()
