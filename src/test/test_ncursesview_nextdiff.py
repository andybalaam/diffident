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

from lib.diffmodels.diffline import DiffLine
from testlib.fakediffmodel import FakeDiffModel

from lib.misc.constants import difflinetypes
from lib.views.ncursesview import NCursesView

def _make_view():
	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( "line 01", "line 01", difflinetypes.IDENTICAL ),
		DiffLine( "line 02", "line 02", difflinetypes.IDENTICAL ),
		DiffLine( "line 03", "line 03", difflinetypes.IDENTICAL ),
		DiffLine( "line 04", "line 04", difflinetypes.IDENTICAL ),
		DiffLine( "line 05", "line 05", difflinetypes.IDENTICAL ),
		DiffLine( "line 06", "line 06", difflinetypes.IDENTICAL ),
		DiffLine( "line 07", "line 07", difflinetypes.IDENTICAL ),
		DiffLine( "line 08", "line 08", difflinetypes.IDENTICAL ),
		DiffLine( "line 09", "line 09", difflinetypes.IDENTICAL ),
		DiffLine( "line 10", "line 10 different", difflinetypes.DIFFERENT ),
		DiffLine( "line 11", "line 11 different", difflinetypes.DIFFERENT ),
		DiffLine( "line 12", "line 12", difflinetypes.IDENTICAL ),
		DiffLine( "line 13", "line 13", difflinetypes.IDENTICAL ),
		DiffLine( None,      "line 14", difflinetypes.ADD ),
		DiffLine( None,      "line 15", difflinetypes.ADD ),
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

	txt, header, status = view.show( actions )

	assert_strings_equal( txt,
"""[n]line 09    line 09  
[d]line 10 [di] * [d]line 10 d
line 11 [di] * [d]line 11 d
[n]line 12    line 12  
line 13    line 13  
[mi]........[ai] + [a]line 14  
[m]........[ai] + [a]line 15  
""" )

	assert_strings_equal( status,
"""[mi] At last difference 
""" )

def next_diff_end_pagedown():

	view = _make_view()

	actions = [ "n", "n", "n", "n", "n", curses.KEY_NPAGE ]

	txt, header, status = view.show( actions )

	assert_strings_equal( txt,
"""[n]line 09    line 09  
[d]line 10 [di] * [d]line 10 d
line 11 [di] * [d]line 11 d
[n]line 12    line 12  
line 13    line 13  
[m]........[ai] + [a]line 14  
[mi]........[ai] + [a]line 15  
""" )

	assert_strings_equal( status,
"""[ni]Press SHIFT-H for he
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

def previous_diff_before_any():

	view = _make_view()

	actions = [ "p" ]

	txt, header, status = view.show( actions )

	assert_strings_equal( txt,
"""[ni]line 01 [n]   line 01  
line 02    line 02  
line 03    line 03  
line 04    line 04  
line 05    line 05  
line 06    line 06  
line 07    line 07  
""" )

	assert_strings_equal( status,
"""[mi]Before first differe
""" )

def _make_diff_at_begin_view():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( "line 01", "line 01 different", difflinetypes.DIFFERENT ),
		DiffLine( "line 02", "line 02 different", difflinetypes.DIFFERENT ),
		DiffLine( "line 03", "line 03 different", difflinetypes.DIFFERENT ),
		DiffLine( "line 04", "line 04", difflinetypes.IDENTICAL ),
		DiffLine( "line 05", "line 05", difflinetypes.IDENTICAL ),
		DiffLine( "line 06", "line 06", difflinetypes.IDENTICAL ),
		DiffLine( "line 07", "line 07", difflinetypes.IDENTICAL ),
		DiffLine( "line 08", "line 08", difflinetypes.IDENTICAL ),
		DiffLine( "line 09", "line 09", difflinetypes.IDENTICAL ),
		DiffLine( "line 10", "line 10 different", difflinetypes.DIFFERENT ),
		DiffLine( "line 11", "line 11 different", difflinetypes.DIFFERENT ),
		DiffLine( "line 12", "line 12", difflinetypes.IDENTICAL ),
		DiffLine( "line 13", "line 13", difflinetypes.IDENTICAL ),
	]

	view = NCursesView( diffmodel )
	view.win_width = 20
	view.win_height = 4

	return view

def next_diff_from_beginning():

	view = _make_diff_at_begin_view()

	actions = [ "n" ]

	txt, header, status = view.show( actions )

	assert_strings_equal( txt,
"""[n]line 07    line 07  
line 08    line 08  
line 09    line 09  
[di]line 10  * [d]line 10 d
""" )

	assert_strings_equal( status,
"""[ni]Press SHIFT-H for he
""" )


def previous_diff_to_beginning():
	"""Track back to the beginning by asking for the previous diff.
	Don't go off to before the beginning."""

	view = _make_diff_at_begin_view()

	actions = [ "n", "n", "p" ]

	txt, header, status = view.show( actions )

	assert_strings_equal( txt,
"""[di]line 01  * [d]line 01 d
line 02 [di] * [d]line 02 d
line 03 [di] * [d]line 03 d
[n]line 04    line 04  
""" )

	assert_strings_equal( status,
"""[ni]Press SHIFT-H for he
""" )

def next_diff_after_last():

	view = _make_diff_at_begin_view()

	actions = [ "n", curses.KEY_DOWN, curses.KEY_DOWN, "n" ]

	txt, header, status = view.show( actions )

	assert_strings_equal( txt,
"""[n]line 09    line 09  
[d]line 10 [di] * [d]line 10 d
line 11 [di] * [d]line 11 d
[ni]line 12 [n]   line 12  
""" )

	assert_strings_equal( status,
"""[mi]After last differenc
""" )

def previous_diff_to_beginning_twice():
	"""Track back to the beginning by asking for the previous diff.
	Don't go off to before the beginning."""

	view = _make_diff_at_begin_view()

	actions = [ "n", "n", "p", "p" ]

	txt, header, status = view.show( actions )

	assert_strings_equal( txt,
"""[di]line 01  * [d]line 01 d
line 02 [di] * [d]line 02 d
line 03 [di] * [d]line 03 d
[n]line 04    line 04  
""" )

	assert_strings_equal( status,
"""[mi]At first difference 
""" )

def _make_manydiffs_view():
	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( "line 01", "line 01", difflinetypes.IDENTICAL ),
		DiffLine( "line 02", "diff 02", difflinetypes.DIFFERENT ),
		DiffLine( "line 03", "diff 03", difflinetypes.DIFFERENT ),
		DiffLine( "line 04", "diff 04", difflinetypes.DIFFERENT ),
		DiffLine( "line 05", "line 05", difflinetypes.IDENTICAL ),
		DiffLine( "line 06", "diff 06", difflinetypes.DIFFERENT ),
		DiffLine( "line 07", "line 07", difflinetypes.IDENTICAL ),
		DiffLine( "line 08", "diff 08", difflinetypes.DIFFERENT ),
		DiffLine( "line 09", "diff 09", difflinetypes.DIFFERENT ),
		DiffLine( "line 10", "diff 10", difflinetypes.DIFFERENT ),
		DiffLine( "line 11", "line 11", difflinetypes.IDENTICAL ),
		DiffLine( "line 12", "diff 12", difflinetypes.DIFFERENT ),
		DiffLine( "line 13", "line 13", difflinetypes.IDENTICAL ),
		DiffLine( "line 14", "line 14", difflinetypes.IDENTICAL ),
		DiffLine( "line 15", "line 15", difflinetypes.IDENTICAL ),
		DiffLine( "line 16", "line 16", difflinetypes.IDENTICAL ),
		DiffLine( "line 17", "line 17", difflinetypes.IDENTICAL ),
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
	next_diff_from_beginning()
	previous_diff_to_beginning()
	previous_diff_to_beginning_twice()
	next_diff_dontmove()
	next_diff_domove_nearend()
	previous_diff_dontmove()
	previous_diff_before_any()
	next_diff_after_last()
	next_diff_end_pagedown()


