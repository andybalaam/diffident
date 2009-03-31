from asserts import assert_strings_equal

from lib.diffmodel import DiffModel
import lib.difflinetypes as difflinetypes

class FakeParser:
	def parse_lines( self, line_callback ):
		line_callback( "line 1\n", "line 1\n", difflinetypes.IDENTICAL )
		line_callback( "line 2 left\n", None, difflinetypes.REMOVE )
		line_callback( None, "line 3 right\n", difflinetypes.ADD )
		line_callback( "line 4 left\n", "line 4 right\n",
			difflinetypes.DIFFERENT )

def get_lines():
	parser = FakeParser()
	diffmodel = DiffModel( parser )
	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left, "line 1" )
	assert_strings_equal( lines[0].right, "line 1" )
	assert( lines[0].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[1].left, "line 2 left" )
	assert_strings_equal( lines[1].right, None )
	assert( lines[1].status == difflinetypes.REMOVE )

	assert_strings_equal( lines[2].left, None )
	assert_strings_equal( lines[2].right, "line 3 right" )
	assert( lines[2].status == difflinetypes.ADD )

	assert_strings_equal( lines[3].left, "line 4 left" )
	assert_strings_equal( lines[3].right, "line 4 right" )
	assert( lines[3].status == difflinetypes.DIFFERENT )

def run():
	get_lines()

