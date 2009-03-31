from test.asserts import assert_strings_equal

import lib.difflinetypes as difflinetypes
from lib.listview import ListView

class FakeDiffModel:
	def __init__( self ):
		self.lines = []

	def get_lines( self ):
		return self.lines

class FakeDiffLine:
	def __init__( self, left, right, status ):
		self.left = left
		self.right = right
		self.status = status

def same():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( "line 1 here", "line 1 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 2 here", "line 2 here", difflinetypes.IDENTICAL ),
		]

	listview = ListView( diffmodel )

	listview.set_columns( 80 )

	assert_strings_equal( listview.get_string(),
"""line 1 here                               line 1 here
line 2 here                               line 2 here
""" )


def just_differences():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( "line 1 here", "line 1 here different",
			difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 2 here", "line 2 here different",
			difflinetypes.DIFFERENT ),
		]

	listview = ListView( diffmodel )

	listview.set_columns( 80 )

	assert_strings_equal( listview.get_string(),
"""line 1 here                            |  line 1 here different
line 2 here                            |  line 2 here different
""" )

	listview.set_columns( 60 )

	assert_strings_equal( listview.get_string(),
"""line 1 here                  |  line 1 here different
line 2 here                  |  line 2 here different
""" )


def run():
	same()
	just_differences()

