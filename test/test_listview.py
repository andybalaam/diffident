from lib.listview import ListView
from test.asserts import assert_strings_equal

class FakeDiffModel:
	def __init__( self ):
		self.lines = []

	def get_lines( self ):
		return self.lines

class FakeDiffLine:
	def __init__( self, left, right ):
		self.left = left
		self.right = right

def just_differences():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( "line 1 here", "line 1 here different" ),
		FakeDiffLine( "line 2 here", "line 2 here different" ),
		]

	listview = ListView( diffmodel )

	listview.set_columns( 80 )

	assert_strings_equal( listview.get_string(),
"""line 1 here                            <> line 1 here different                 
line 2 here                            <> line 2 here different                 
""" )

	listview.set_columns( 60 )

	assert_strings_equal( listview.get_string(),
"""line 1 here                  <> line 1 here different       
line 2 here                  <> line 2 here different       
""" )


def run():
	just_differences()

