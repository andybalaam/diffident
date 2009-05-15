#   Diffident, an interactive diff viewer and editor
#   Copyright (C) 2009 Andy Balaam <axis3x3@users.sf.net>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from test.asserts import assert_strings_equal

from lib.diffline import DiffLine
from testlib.fakediffmodel import FakeDiffModel

from lib.constants import difflinetypes
from lib.listview import ListView

def same():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( "line 1 here", "line 1 here", difflinetypes.IDENTICAL ),
		DiffLine( "line 2 here", "line 2 here", difflinetypes.IDENTICAL ),
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
		DiffLine( "line 1 here", "line 1 here different",
			difflinetypes.DIFFERENT ),
		DiffLine( "line 2 here", "line 2 here different",
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
		DiffLine( None, "line 1 here", difflinetypes.ADD ),
		DiffLine( None, "line 2 here", difflinetypes.ADD ),
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
		DiffLine( "line 1 here", None, difflinetypes.REMOVE ),
		DiffLine( "line 2 here", None, difflinetypes.REMOVE ),
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

