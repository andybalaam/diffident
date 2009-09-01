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

from lib.misc.constants import directions
from lib.misc.constants import difflinetypes

from lib.views.ncursesview import NCursesView

class EditTracingFakeDiffModel( FakeDiffModel ):
	def __init__( self ):
		super( EditTracingFakeDiffModel, self ).__init__()
		self.trace = []

	def edit_lines( self, first_line_num, last_line_num, side, lines ):
		self.trace.append( ( "edit_lines", first_line_num, last_line_num, side,
			lines ) )

	def delete_lines( self, first_line_num, last_line_num, side ):
		self.trace.append( ( "delete_lines",
			first_line_num, last_line_num, side ) )

	def add_lines( self, before_line_num, side, strs ):
		self.trace.append( ( "add_lines",
			before_line_num, side, strs ) )

class EditReportingFakeDiffModel( FakeDiffModel ):
	def __init__( self ):
		super( EditReportingFakeDiffModel, self ).__init__()
		self.has_edit = {
			directions.LEFT : False,
			directions.RIGHT : True,
			}

	def has_edit_affecting_side( self, side ):
		return self.has_edit[side]

def _make_view():
	diffmodel = EditTracingFakeDiffModel()
	diffmodel.lines = [
		DiffLine( "left 01", "right 01", difflinetypes.DIFFERENT ),
		DiffLine( "left 02", "right 02", difflinetypes.DIFFERENT ),
		DiffLine( "left 03", "right 03", difflinetypes.DIFFERENT ),
		DiffLine( "left 04", "right 04", difflinetypes.DIFFERENT ),
		DiffLine( "left 05", "right 05", difflinetypes.DIFFERENT ),
		DiffLine( "left 06", "right 06", difflinetypes.DIFFERENT ),
		DiffLine( "left 07", "right 07", difflinetypes.DIFFERENT ),
		DiffLine( "left 08", "right 08", difflinetypes.DIFFERENT ),
		DiffLine( "left 09", "right 09", difflinetypes.DIFFERENT ),
		DiffLine( "left 10", "right 10", difflinetypes.DIFFERENT ),
		DiffLine( "left 11", "right 11", difflinetypes.DIFFERENT ),
		DiffLine( "left 12", "right 12", difflinetypes.DIFFERENT ),
	]

	view = NCursesView( diffmodel )
	view.win_width = 20
	view.win_height = 5

	return view, diffmodel

def copy_l2r_1_line():

	view, diffmodel = _make_view()
	actions = [ "j", "]" ]
	view.show( actions )

	assert( diffmodel.trace ==
		[ ( "edit_lines", 1, 1, directions.RIGHT, [ "left 02" ] ),
		] )

def copy_r2l_multiple_lines_upside_down_after_scroll():

	view, diffmodel = _make_view()
	actions = [ "j", "l", "j", "j", "j", "j", "K", "K", "[" ]
	view.show( actions )

	assert( diffmodel.trace ==
		[ ( "edit_lines", 3, 5, directions.LEFT, [
			"right 04",
			"right 05",
			"right 06", ] ),
		] )

def delete_lines():
	view, diffmodel = _make_view()
	actions = [ "j", "l", "j", "j", "j", "j", "K", "K", "d" ]
	view.show( actions )

	assert( diffmodel.trace ==
		[ ( "delete_lines", 3, 5, directions.RIGHT ),
		] )

def add_lines():
	view, diffmodel = _make_view()
	actions = [ curses.KEY_NPAGE, "k", "k", "a", "j", "j", "a", "l", "k", "a" ]
	view.show( actions )

	assert( diffmodel.trace ==
		[ ( "add_lines", 3, directions.LEFT, ('',) ),
		  ( "add_lines", 5, directions.LEFT, ('',) ),
		  ( "add_lines", 4, directions.RIGHT, ('',) ),
		] )

def display_edited_lines():
	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( "left 01", "right 01", difflinetypes.DIFFERENT, False, True ),
		DiffLine( "left 02", "right 02", difflinetypes.DIFFERENT, True,  True ),
		DiffLine( "left 03", "right 03", difflinetypes.DIFFERENT, True, False ),
		DiffLine( "line 04", "line 04",  difflinetypes.IDENTICAL, False, True ),
		DiffLine( "line 05", "line 05",  difflinetypes.IDENTICAL, True,  True ),
		DiffLine( "line 06", "line 06",  difflinetypes.IDENTICAL, True, False ),
	]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 6

	actions = []

	assert_strings_equal( view.show( actions )[0],
"""[di]left 01           [ei] * [e]right 01           
left 02           [ei] * [e]right 02           
left 03           [ei] * [d]right 03           
[n]line 04           [ei]   [e]line 04            
line 05           [ei]   [e]line 05            
line 06           [ei]   [n]line 06            
""" )

def display_file_modified_left_short():

	diffmodel = EditReportingFakeDiffModel()
	diffmodel.has_edit[ directions.LEFT ] = True
	diffmodel.has_edit[ directions.RIGHT ] = False

	view = NCursesView( diffmodel )
	view.win_width = 30
	view.win_height = 5
	view.filename_left = "/path/to/the/filename_left.txt"
	view.filename_right = "r.txt"

	actions = []
	(window, header, status ) = view.show( actions )

	assert_strings_equal( header,
		"[ni]*..._left.txt   r.txt         \n" )


def display_file_modified_right():

	diffmodel = EditReportingFakeDiffModel()
	diffmodel.has_edit[ directions.LEFT ] = False
	diffmodel.has_edit[ directions.RIGHT ] = True

	view = NCursesView( diffmodel )
	view.win_width = 60
	view.win_height = 5
	view.filename_left = "filename_left.txt"
	view.filename_right = "filename_right.txt"

	actions = []
	(window, header, status ) = view.show( actions )

	assert_strings_equal( header,
		"[ni]filename_left.txt              *filename_right.txt          \n" )

def display_file_modified_both():

	diffmodel = EditReportingFakeDiffModel()
	diffmodel.has_edit[ directions.LEFT ] = True
	diffmodel.has_edit[ directions.RIGHT ] = True

	view = NCursesView( diffmodel )
	view.win_width = 60
	view.win_height = 5
	view.filename_left = "filename_left.txt"
	view.filename_right = "filename_right.txt"

	actions = []
	(window, header, status ) = view.show( actions )

	assert_strings_equal( header,
		"[ni]*filename_left.txt             *filename_right.txt          \n" )

def run():
	copy_l2r_1_line()
	copy_r2l_multiple_lines_upside_down_after_scroll()
	delete_lines()
	display_edited_lines()
	display_file_modified_left_short()
	display_file_modified_right()
	display_file_modified_both()
	add_lines()

