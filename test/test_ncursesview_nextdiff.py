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

	assert_strings_equal( view.show( actions )[0],
"""[n]line 07    line 07  
line 08    line 08  
line 09    line 09  
[di]line 10  * [d]line 10 d
line 11 [di] * [d]line 11 d
[n]line 12    line 12  
line 13    line 13  
""" )

def next_diff_several():

	view = _make_view()

	actions = [ curses.KEY_RIGHT, "n", "n" ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 09    line 09  
[d]line 10 [di] * [d]line 10 d
line 11 [di] * [d]line 11 d
[n]line 12    line 12  
line 13    line 13  
[m]........[ai] + line 14  
[m]........[ai] + [a]line 15  
""" )

def next_diff_end():

	view = _make_view()

	actions = [ "n", "n", "n", "n", "n" ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 09    line 09  
[d]line 10 [di] * [d]line 10 d
line 11 [di] * [d]line 11 d
[n]line 12    line 12  
line 13    line 13  
[mi]........[ai] + [a]line 14  
[m]........[ai] + [a]line 15  
""" )

def previous_diff():

	view = _make_view()

	actions = [ "n", "n", curses.KEY_DOWN, "p" ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 09    line 09  
[di]line 10  * [d]line 10 d
line 11 [di] * [d]line 11 d
[n]line 12    line 12  
line 13    line 13  
[m]........[ai] + [a]line 14  
[m]........[ai] + [a]line 15  
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

	assert_strings_equal( view.show( actions )[0],
"""[di]line 01  * [d]line 01 d
line 02 [di] * [d]line 02 d
line 03 [di] * [d]line 03 d
""" )

def previous_diff_to_beginning_twice():
	"""Track back to the beginning by asking for the previous diff.
	Don't go off to before the beginning."""

	view = _make_diff_at_begin_view()

	actions = [ "n", "n", "p", "p" ]

	assert_strings_equal( view.show( actions )[0],
"""[di]line 01  * [d]line 01 d
line 02 [di] * [d]line 02 d
line 03 [di] * [d]line 03 d
""" )

def _make_manydiffs_view():
	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( "line 01", "line 01", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 02", "diff 02", difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 03", "diff 03", difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 04", "diff 04", difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 05", "line 05", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 06", "diff 06", difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 07", "line 07", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 08", "diff 08", difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 09", "diff 09", difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 10", "diff 10", difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 11", "line 11", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 12", "diff 12", difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 13", "line 13", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 14", "line 14", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 15", "line 15", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 16", "line 16", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 17", "line 17", difflinetypes.IDENTICAL ),
	]

	view = NCursesView( diffmodel )
	view.win_width = 20
	view.win_height = 10

	return view

def next_diff_dontmove():
	view = _make_manydiffs_view()

	actions = [ "n", "n" ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 01    line 01  
[d]line 02 [di] * [d]diff 02  
line 03 [di] * [d]diff 03  
line 04 [di] * [d]diff 04  
[n]line 05    line 05  
[di]line 06  * [d]diff 06  
[n]line 07    line 07  
[d]line 08 [di] * [d]diff 08  
line 09 [di] * [d]diff 09  
line 10 [di] * [d]diff 10  
""" )

def next_diff_domove_nearend():
	view = _make_manydiffs_view()

	actions = [ "n", "n", "n" ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 05    line 05  
[d]line 06 [di] * [d]diff 06  
[n]line 07    line 07  
[di]line 08  * [d]diff 08  
line 09 [di] * [d]diff 09  
line 10 [di] * [d]diff 10  
[n]line 11    line 11  
[d]line 12 [di] * [d]diff 12  
[n]line 13    line 13  
line 14    line 14  
""" )

def previous_diff_dontmove():
	view = _make_manydiffs_view()

	actions = [ "n", "n", "n", "p" ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 05    line 05  
[di]line 06  * [d]diff 06  
[n]line 07    line 07  
[d]line 08 [di] * [d]diff 08  
line 09 [di] * [d]diff 09  
line 10 [di] * [d]diff 10  
[n]line 11    line 11  
[d]line 12 [di] * [d]diff 12  
[n]line 13    line 13  
line 14    line 14  
""" )


def run():
	next_diff_different()
	next_diff_several()
	next_diff_end()
	previous_diff()
	previous_diff_to_beginning()
	previous_diff_to_beginning_twice()
	next_diff_dontmove()
	next_diff_domove_nearend()
	previous_diff_dontmove()

