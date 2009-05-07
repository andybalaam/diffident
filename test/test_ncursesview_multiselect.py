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

def cursor_get_selected_range():
	l = NCursesView.LEFT

	curs = NCursesView.Cursor( l, 10 )
	curs.start_line_num = 10
	curs.line_num = 10
	assert( tuple( curs.get_selected_range() ) == ( 10, ) )

	curs.start_line_num = 10
	curs.line_num = 12
	assert( tuple( curs.get_selected_range() ) == ( 10, 11, 12 ) )

	curs.start_line_num = 14
	curs.line_num = 12
	assert( tuple( curs.get_selected_range() ) == ( 12, 13, 14 ) )

	curs.start_line_num = -1
	curs.line_num = 2
	assert( tuple( curs.get_selected_range() ) == ( -1, 0, 1, 2 ) )

	curs.start_line_num = 2
	curs.line_num = -1
	assert( tuple( curs.get_selected_range() ) == ( -1, 0, 1, 2 ) )

def _make_view():
	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( "line 1 here", "line 1 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 2 here", "line 2 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 3 here", "line 3 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 4 here", "line 4 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 5 here", "line 5 here different",
			difflinetypes.DIFFERENT ),
		FakeDiffLine( "line 6 here", "line 6 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 7 here", "line 7 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 8 here", "line 8 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 9 here", "line 9 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 10 here", "line 10 here", difflinetypes.IDENTICAL ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 5

	return view


def normal_down():
	view = _make_view()

	actions = [ "j", "J", "J" ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 1 here          line 1 here        
[ni]line 2 here       [n]   line 2 here        
[ni]line 3 here       [n]   line 3 here        
[ni]line 4 here       [n]   line 4 here        
[d]line 5 here       [di] * [d]line 5 here differe
""" )

	assert( view.mycursor.start_line_num == 1 )
	assert( view.mycursor.line_num       == 3 )


def normal_up():
	view = _make_view()

	actions = [ "j", "j", "K" ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 1 here          line 1 here        
[ni]line 2 here       [n]   line 2 here        
[ni]line 3 here       [n]   line 3 here        
line 4 here          line 4 here        
[d]line 5 here       [di] * [d]line 5 here differe
""" )

	assert( view.mycursor.start_line_num == 2 )
	assert( view.mycursor.line_num       == 1 )

def lose_when_release_shift_up():
	view = _make_view()

	actions = [ "j", "J", "J", "k" ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 1 here          line 1 here        
line 2 here          line 2 here        
[ni]line 3 here       [n]   line 3 here        
line 4 here          line 4 here        
[d]line 5 here       [di] * [d]line 5 here differe
""" )

	assert( view.mycursor.start_line_num == 2 )
	assert( view.mycursor.line_num       == 2 )


def lose_when_release_shift_down():
	view = _make_view()

	actions = [ "j", "J", "J", "j" ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 1 here          line 1 here        
line 2 here          line 2 here        
line 3 here          line 3 here        
line 4 here          line 4 here        
[di]line 5 here        * [d]line 5 here differe
""" )

	assert( view.mycursor.start_line_num == 4 )
	assert( view.mycursor.line_num       == 4 )

def lose_when_release_shift_right():
	view = _make_view()

	actions = [ "j", "J", "J", "l" ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 1 here          line 1 here        
line 2 here          line 2 here        
line 3 here          line 3 here        
line 4 here          [ni]line 4 here        
[d]line 5 here       [di] * [d]line 5 here differe
""" )

	assert( view.mycursor.start_line_num == 3 )
	assert( view.mycursor.line_num       == 3 )

def lose_when_release_shift_n():
	view = _make_view()

	actions = [ "j", "J", "J", "n" ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 2 here          line 2 here        
line 3 here          line 3 here        
line 4 here          line 4 here        
[di]line 5 here        * [d]line 5 here differe
[n]line 6 here          line 6 here        
""" )

	assert( view.mycursor.start_line_num == 3 )
	assert( view.mycursor.line_num       == 3 )


def lose_when_release_shift_pagedown():
	view = _make_view()

	actions = [ "j", "J", "J", curses.KEY_NPAGE ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 6 here          line 6 here        
line 7 here          line 7 here        
line 8 here          line 8 here        
[ni]line 9 here       [n]   line 9 here        
line 10 here         line 10 here       
""" )

	assert( view.mycursor.start_line_num == 3 )
	assert( view.mycursor.line_num       == 3 )




def normal_on_right():
	view = _make_view()

	actions = [ "l", "j", "J", "J" ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 1 here          line 1 here        
line 2 here          [ni]line 2 here        
[n]line 3 here          [ni]line 3 here        
[n]line 4 here          [ni]line 4 here        
[d]line 5 here       [di] * [d]line 5 here differe
""" )

	assert( view.mycursor.start_line_num == 1 )
	assert( view.mycursor.line_num       == 3 )

def lose_when_release_shift_left_on_right():
	view = _make_view()

	actions = [ "l", "j", "J", "J", "h" ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 1 here          line 1 here        
line 2 here          line 2 here        
line 3 here          line 3 here        
[ni]line 4 here       [n]   line 4 here        
[d]line 5 here       [di] * [d]line 5 here differe
""" )

	assert( view.mycursor.start_line_num == 3 )
	assert( view.mycursor.line_num       == 3 )

def hit_bottom():
	view = _make_view()

	actions = [ curses.KEY_NPAGE, "j", "j", "J", "J", "J", "J" ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 6 here          line 6 here        
line 7 here          line 7 here        
[ni]line 8 here       [n]   line 8 here        
[ni]line 9 here       [n]   line 9 here        
[ni]line 10 here      [n]   line 10 here       
""" )

	assert( view.mycursor.start_line_num == 2 )
	assert( view.mycursor.line_num       == 4 )

def _make_shortdiff_view():
	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		FakeDiffLine( "line 1 here", "line 1 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 2 here", "line 2 here", difflinetypes.IDENTICAL ),
		FakeDiffLine( "line 3 here", "line 3 here", difflinetypes.IDENTICAL ),
		]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 5

	return view



def hit_bottom_shortdiff():
	view = _make_shortdiff_view()

	actions = [ "j", "J", "J", ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 1 here          line 1 here        
[ni]line 2 here       [n]   line 2 here        
[ni]line 3 here       [n]   line 3 here        
                                        
                                        
""" )

	assert( view.mycursor.start_line_num == 1 )
	assert( view.mycursor.line_num       == 2 )


def hit_top():
	view = _make_shortdiff_view()

	actions = [ "K", "K" ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]line 1 here       [n]   line 1 here        
line 2 here          line 2 here        
line 3 here          line 3 here        
                                        
                                        
""" )

	assert( view.mycursor.start_line_num == 0 )
	assert( view.mycursor.line_num       == 0 )



def scroll_down():
	view = _make_view()

	actions = [ "j", "j", "j", "J", "J", ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 2 here          line 2 here        
line 3 here          line 3 here        
[ni]line 4 here       [n]   line 4 here        
[di]line 5 here        * [d]line 5 here differe
[ni]line 6 here       [n]   line 6 here        
""" )

	assert( view.mycursor.start_line_num == 2 )
	assert( view.mycursor.line_num       == 4 )


def scroll_up():
	view = _make_view()

	actions = [ curses.KEY_NPAGE, "K", "K" ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]line 4 here       [n]   line 4 here        
[di]line 5 here        * [d]line 5 here differe
[ni]line 6 here       [n]   line 6 here        
line 7 here          line 7 here        
line 8 here          line 8 here        
""" )

	assert( view.mycursor.start_line_num == 2 )
	assert( view.mycursor.line_num       == 0 )


def down_more_than_one_screen():
	view = _make_view()

	actions = [ "j", "J", "J", "J", "J", "J", "J" ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]line 4 here       [n]   line 4 here        
[di]line 5 here        * [d]line 5 here differe
[ni]line 6 here       [n]   line 6 here        
[ni]line 7 here       [n]   line 7 here        
[ni]line 8 here       [n]   line 8 here        
""" )

	assert( view.mycursor.start_line_num == -2 )
	assert( view.mycursor.line_num       ==  4 )


def up_more_than_one_screen():
	view = _make_view()

	actions = [ curses.KEY_NPAGE, curses.KEY_NPAGE, curses.KEY_NPAGE,
		"k", "K", "K", "K", "K", "K", "K", "K", ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]line 2 here       [n]   line 2 here        
[ni]line 3 here       [n]   line 3 here        
[ni]line 4 here       [n]   line 4 here        
[di]line 5 here        * [d]line 5 here differe
[ni]line 6 here       [n]   line 6 here        
""" )

	assert( view.mycursor.start_line_num == 7 )
	assert( view.mycursor.line_num       == 0 )


def shift_pagedown():
	view = _make_view()

	actions = [ "j", ">" ]

	assert_strings_equal( view.show( actions )[0],
"""[ni]line 6 here       [n]   line 6 here        
[ni]line 7 here       [n]   line 7 here        
line 8 here          line 8 here        
line 9 here          line 9 here        
line 10 here         line 10 here       
""" )

	assert( view.mycursor.start_line_num == -4 )
	assert( view.mycursor.line_num       ==  1 )



def shift_pageup():
	view = _make_view()

	actions = [ curses.KEY_NPAGE, curses.KEY_NPAGE, curses.KEY_NPAGE, "<" ]

	assert_strings_equal( view.show( actions )[0],
"""[n]line 1 here          line 1 here        
line 2 here          line 2 here        
line 3 here          line 3 here        
line 4 here          line 4 here        
[di]line 5 here        * [d]line 5 here differe
""" )

	assert( view.mycursor.start_line_num == 9 )
	assert( view.mycursor.line_num       == 4 )



def run():
	cursor_get_selected_range()
	normal_down()
	normal_up()
	lose_when_release_shift_up()
	lose_when_release_shift_down()
	lose_when_release_shift_right()
	lose_when_release_shift_n()
	lose_when_release_shift_pagedown()
	normal_on_right()
	lose_when_release_shift_left_on_right()
	hit_bottom()
	hit_bottom_shortdiff()
	hit_top()
	scroll_down()
	scroll_up()
	down_more_than_one_screen()
	up_more_than_one_screen()
	shift_pagedown()
	shift_pageup()


