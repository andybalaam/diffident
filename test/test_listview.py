from test.asserts import assert_strings_equal

from testlib.fakediffline import FakeDiffLine
from testlib.fakediffmodel import FakeDiffModel

import lib.difflinetypes as difflinetypes
from lib.listview import ListView

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


def differences():

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

def adds():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( None, "line 1 here", difflinetypes.ADD ),
		FakeDiffLine( None, "line 2 here", difflinetypes.ADD ),
		]

	listview = ListView( diffmodel )

	listview.set_columns( 80 )

	assert_strings_equal( listview.get_string(),
"""                                       >  line 1 here
                                       >  line 2 here
""" )


def removes():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( "line 1 here", None, difflinetypes.REMOVE ),
		FakeDiffLine( "line 2 here", None, difflinetypes.REMOVE ),
		]

	listview = ListView( diffmodel )

	listview.set_columns( 80 )

	assert_strings_equal( listview.get_string(),
"""line 1 here                            <
line 2 here                            <
""" )



def run():
	same()
	differences()
	adds()
	removes()

