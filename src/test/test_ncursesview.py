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

from lib.diffmodels.diffline import DiffLine
from testlib.fakediffmodel import FakeDiffModel

from lib.misc.constants import difflinetypes
from lib.views.ncursesview import NCursesView

def pad_to_width():
	diffmodel = FakeDiffModel()
	view = NCursesView( diffmodel )

	assert_strings_equal( view.pad_to_width( None, 0, 5 ), "....." )
	assert_strings_equal( view.pad_to_width( "d f", 0, 5 ), "d f  " )
	assert_strings_equal( view.pad_to_width( "d fffffffff", 0, 5 ),
		"d fffffffff" )

	assert_strings_equal( view.pad_to_width( "d fffffffff", 3, 5 ), "ffffffff" )

def same():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( "line 1 here", "line 1 here", difflinetypes.IDENTICAL ),
		DiffLine( "line 2 here", "line 2 here", difflinetypes.IDENTICAL ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 5

	actions = []

	assert_strings_equal( view.show( actions )[0],
"""[ni]line 1 here       [n]   line 1 here        
line 2 here          line 2 here        
                                        
                                        
                                        
""" )


def differences():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( "line 1 here", "line 1 here different",
			difflinetypes.DIFFERENT ),
		DiffLine( "line 2 here", "line 2 here different",
			difflinetypes.DIFFERENT ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 5

	actions = []

	assert_strings_equal( view.show( actions )[0],
"""[di]line 1 here        * [d]line 1 here differe
line 2 here       [di] * [d]line 2 here differe
[n]                                        
                                        
                                        
""" )

def adds():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( None, "line 1 here",
			difflinetypes.ADD ),
		DiffLine( None, "line 2 here",
			difflinetypes.ADD ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 5

	actions = []

	assert_strings_equal( view.show( actions )[0],
"""[mi]..................[ai] + [a]line 1 here        
[m]..................[ai] + [a]line 2 here        
[n]                                        
                                        
                                        
""" )

def removes():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( "line 1 here", None,
			difflinetypes.REMOVE ),
		DiffLine( "line 2 here", None,
			difflinetypes.REMOVE ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 39
	view.win_height = 5

	actions = []

	assert_strings_equal( view.show( actions )[0],
"""[ri]line 1 here        - [m]..................
[r]line 2 here       [ri] - [m]..................
[n]                                       
                                       
                                       
""" )




def mixture():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( "line 1 here", "line 1 here", difflinetypes.IDENTICAL ),
		DiffLine( None, "line 2 here",
			difflinetypes.ADD ),
		DiffLine( "line 3 here", "line 3 here", difflinetypes.IDENTICAL ),
		DiffLine( "line 4 here", "line 4 here different",
			difflinetypes.DIFFERENT ),
		DiffLine( "line 5 here", None,
			difflinetypes.REMOVE ),
		DiffLine( "line 6 here", "line 6 here", difflinetypes.IDENTICAL ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 5

	actions = []

	assert_strings_equal( view.show( actions )[0],
"""[ni]line 1 here       [n]   line 1 here        
[m]..................[ai] + [a]line 2 here        
[n]line 3 here          line 3 here        
[d]line 4 here       [di] * [d]line 4 here differe
[r]line 5 here       [ri] - [m]...................
""" )

def run():
	pad_to_width()
	same()
	differences()
	adds()
	removes()
	mixture()

