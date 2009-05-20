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

import itertools

from asserts import assert_strings_equal

from lib.diffline import DiffLine
from testlib.fakediffmodel import FakeDiffModel

from lib.constants import difflinetypes
from lib.constants import directions

from lib.editablediffmodel import EditableDiffModel

from lib.listview import ListView # TODO: remove this

def _make_static_diffmodel():
	staticdiffmodel = FakeDiffModel()
	staticdiffmodel.lines = [
		DiffLine( "line 1 here", "line 1 here", difflinetypes.IDENTICAL ),
		DiffLine( "line 2 here", "line 2 here", difflinetypes.IDENTICAL ),
		DiffLine( "line 3 here", "line 3 here", difflinetypes.IDENTICAL ),
		DiffLine( "line 4 here", "line 4 here", difflinetypes.IDENTICAL ),
		DiffLine( "line 5 here", "line 5 here different",
			difflinetypes.DIFFERENT ),
		DiffLine( "line 6 here", "line 6 here", difflinetypes.IDENTICAL ),
		DiffLine( "line 7 here", "line 7 here", difflinetypes.IDENTICAL ),
		DiffLine( "line 8 here", "line 8 here", difflinetypes.IDENTICAL ),
		DiffLine( "line 9 here", "line 9 here", difflinetypes.IDENTICAL ),
		DiffLine( "previous 10", "line 10 here", difflinetypes.DIFFERENT ),
		]

	return staticdiffmodel

def _print_lines_list( lst ):
	for line in lst:
		print line

def _lines_lists_equal( lst1, lst2 ):
	if len( lst1 ) != len( lst2 ):
		return False

	for line1, line2 in itertools.izip( lst1, lst2 ):
		if line1.left != line2.left:
			return False
		if line1.right != line2.right:
			return False
		if line1.status != line2.status:
			return False
		if "left_edited" in line1.__dict__:
			if "left_edited" not in line2.__dict__:
				return False
			if line1.left_edited != line2.left_edited:
				return False
		if "right_edited" in line1.__dict__:
			if "right_edited" not in line2.__dict__:
				return False
			if line1.right_edited != line2.right_edited:
				return False
	return True

def assert_lines_lists_equal( lst1, lst2 ):
	if not _lines_lists_equal( lst1, lst2 ):
		_print_lines_list( lst1 )
		print "Differs from:"
		_print_lines_list( lst2 )
		raise AssertionError()

def edit_line():
	staticdiffmodel = _make_static_diffmodel()
	old_static_lines = list( ln.clone() for ln in staticdiffmodel.get_lines() )

	editable = EditableDiffModel( staticdiffmodel )

	# Change one line
	editable.edit_lines( 3, 3, directions.RIGHT, ( "edited", ) )

	# The line before is unchanged
	ln = editable.get_line( 2 )
	assert_strings_equal( ln.left, "line 3 here" )
	assert_strings_equal( ln.right, "line 3 here" )
	assert( ln.status == difflinetypes.IDENTICAL )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )

	# The line itself is changed, and marked as EDITED
	ln = editable.get_line( 3 )
	assert_strings_equal( ln.left, "line 4 here" )
	assert_strings_equal( ln.right, "edited" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == True )

	# The line after is unchanged
	ln = editable.get_line( 4 )
	assert_strings_equal( ln.left, "line 5 here" )
	assert_strings_equal( ln.right, "line 5 here different" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )

	# The underlying diffmodel has not been altered
	assert_lines_lists_equal( old_static_lines, staticdiffmodel.get_lines() )

def edit_several_lines():
	staticdiffmodel = _make_static_diffmodel()
	old_static_lines = list( ln.clone() for ln in staticdiffmodel.get_lines() )

	editable = EditableDiffModel( staticdiffmodel )

	# Change 3 lines
	editable.edit_lines( 7, 9, directions.LEFT,
		( "edited 8", "edited 9", "line 10 here" ) )

	lines = editable.get_lines()

	#print ListView( editable ).get_string()

	# The line before is unchanged
	assert_strings_equal( lines[6].left, "line 7 here" )
	assert_strings_equal( lines[6].right, "line 7 here" )
	assert( lines[6].status == difflinetypes.IDENTICAL )
	assert( lines[6].left_edited == False )
	assert( lines[6].right_edited == False )

	# The relevant lines have been changed
	assert_strings_equal( lines[7].left, "edited 8" )
	assert_strings_equal( lines[7].right, "line 8 here" )
	assert( lines[7].status == difflinetypes.DIFFERENT )
	assert( lines[7].left_edited == True )
	assert( lines[7].right_edited == False )

	assert_strings_equal( lines[8].left, "edited 9" )
	assert_strings_equal( lines[8].right, "line 9 here" )
	assert( lines[8].status == difflinetypes.DIFFERENT )
	assert( lines[8].left_edited == True )
	assert( lines[8].right_edited == False )

	assert_strings_equal( lines[9].left, "line 10 here" )
	assert_strings_equal( lines[9].right, "line 10 here" )
	assert( lines[9].status == difflinetypes.IDENTICAL )
	assert( lines[9].left_edited == True )
	assert( lines[9].right_edited == False )

	# The underlying diffmodel has not been altered
	assert_lines_lists_equal( old_static_lines, staticdiffmodel.get_lines() )

def edit_both_sides():
	staticdiffmodel = _make_static_diffmodel()
	old_static_lines = list( ln.clone() for ln in staticdiffmodel.get_lines() )

	editable = EditableDiffModel( staticdiffmodel )

	# Change 3 lines on left sides
	editable.edit_lines( 7, 9, directions.LEFT,
		( "edited 8", "edited 9", "edited 10" ) )

	# and 4 lines (overlapping) on right
	editable.edit_lines( 6, 9, directions.RIGHT,
		( "edited 7", "edited 8 r", "edited 9", "edited 10 r" ) )

	lines = editable.get_lines()

	#print ListView( editable ).get_string()

	# The line before is unchanged
	assert_strings_equal( lines[6].left, "line 7 here" )
	assert_strings_equal( lines[6].right, "edited 7" )
	assert( lines[6].status == difflinetypes.DIFFERENT )
	assert( lines[6].left_edited == False )
	assert( lines[6].right_edited == True )

	# The relevant lines have been changed
	assert_strings_equal( lines[7].left, "edited 8" )
	assert_strings_equal( lines[7].right, "edited 8 r" )
	assert( lines[7].status == difflinetypes.DIFFERENT )
	assert( lines[7].left_edited == True )
	assert( lines[7].right_edited == True )

	assert_strings_equal( lines[8].left, "edited 9" )
	assert_strings_equal( lines[8].right, "edited 9" )
	assert( lines[8].status == difflinetypes.IDENTICAL )
	assert( lines[8].left_edited == True )
	assert( lines[8].right_edited == True )

	assert_strings_equal( lines[9].left, "edited 10" )
	assert_strings_equal( lines[9].right, "edited 10 r" )
	assert( lines[9].status == difflinetypes.DIFFERENT )
	assert( lines[9].left_edited == True )
	assert( lines[9].right_edited == True )

	# The underlying diffmodel has not been altered
	assert_lines_lists_equal( old_static_lines, staticdiffmodel.get_lines() )

def edit_starts_before():
	staticdiffmodel = _make_static_diffmodel()

	editable = EditableDiffModel( staticdiffmodel )

	# Change 3 lines
	editable.edit_lines( 6, 9, directions.RIGHT,
		( "edited 7", "edited 8", "edited 9", "edited 10" ) )

	# Just ask for lines 8 and 9
	lines = editable.get_lines( 8 )

	assert_strings_equal( lines[0].left, "line 9 here" )
	assert_strings_equal( lines[0].right, "edited 9" )
	assert( lines[0].status == difflinetypes.DIFFERENT )
	assert( lines[0].left_edited == False )
	assert( lines[0].right_edited == True )

	assert_strings_equal( lines[1].left, "previous 10" )
	assert_strings_equal( lines[1].right, "edited 10" )
	assert( lines[1].status == difflinetypes.DIFFERENT )
	assert( lines[1].left_edited == False )
	assert( lines[1].right_edited == True )

def edit_ends_after():
	staticdiffmodel = _make_static_diffmodel()

	editable = EditableDiffModel( staticdiffmodel )

	# Change 3 lines
	editable.edit_lines( 6, 9, directions.RIGHT,
		( "edited 7", "edited 8", "edited 9", "edited 10" ) )

	# Just ask for lines 6 and 7
	lines = editable.get_lines( 5, 7 )

	assert_strings_equal( lines[0].left, "line 6 here" )
	assert_strings_equal( lines[0].right, "line 6 here" )
	assert( lines[0].status == difflinetypes.IDENTICAL )
	assert( lines[0].left_edited == False )
	assert( lines[0].right_edited == False )

	assert_strings_equal( lines[1].left, "line 7 here" )
	assert_strings_equal( lines[1].right, "edited 7" )
	assert( lines[1].status == difflinetypes.DIFFERENT )
	assert( lines[1].left_edited == False )
	assert( lines[1].right_edited == True )

def edit_spans_before_and_after():
	staticdiffmodel = _make_static_diffmodel()

	editable = EditableDiffModel( staticdiffmodel )

	# Change all 10 lines
	editable.edit_lines( 0, 9, directions.RIGHT,
		( "edited 1", "edited 2", "edited 3", "edited 4", "edited 5",
		  "edited 6", "edited 7", "edited 8", "edited 9", "edited 10" ) )

	# Just ask for lines 7, 8 and 9
	lines = editable.get_lines( 6, 10 )

	assert_strings_equal( lines[0].left, "line 7 here" )
	assert_strings_equal( lines[0].right, "edited 7" )
	assert( lines[0].status == difflinetypes.DIFFERENT )
	assert( lines[0].left_edited == False )
	assert( lines[0].right_edited == True )

	assert_strings_equal( lines[1].left, "line 8 here" )
	assert_strings_equal( lines[1].right, "edited 8" )
	assert( lines[1].status == difflinetypes.DIFFERENT )
	assert( lines[1].left_edited == False )
	assert( lines[1].right_edited == True )

	assert_strings_equal( lines[2].left, "line 9 here" )
	assert_strings_equal( lines[2].right, "edited 9" )
	assert( lines[2].status == difflinetypes.DIFFERENT )
	assert( lines[2].left_edited == False )
	assert( lines[2].right_edited == True )

	ln = editable.get_line( 0 )
	assert_strings_equal( ln.left, "line 1 here" )
	assert_strings_equal( ln.right, "edited 1" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == True )

def edit_doesnt_touch():
	staticdiffmodel = _make_static_diffmodel()

	editable = EditableDiffModel( staticdiffmodel )

	# Change 3 lines
	editable.edit_lines( 1, 3, directions.RIGHT,
		( "edited 2", "edited 3", "edited 4" ) )

	# Just ask for line 9
	lines = editable.get_lines( 9, 10 )

	assert_strings_equal( lines[0].left, "previous 10" )
	assert_strings_equal( lines[0].right, "line 10 here" )
	assert( lines[0].status == difflinetypes.DIFFERENT )
	assert( lines[0].left_edited == False )
	assert( lines[0].right_edited == False )

	ln = editable.get_line( 8 )
	assert_strings_equal( ln.left, "line 9 here" )
	assert_strings_equal( ln.right, "line 9 here" )
	assert( ln.status == difflinetypes.IDENTICAL )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )

def several_edits():
	staticdiffmodel = _make_static_diffmodel()
	old_static_lines = list( ln.clone() for ln in staticdiffmodel.get_lines() )

	editable = EditableDiffModel( staticdiffmodel )

	# Make several overlapping changes
	editable.edit_lines( 0, 2, directions.RIGHT,
		( "edited 1a", "edited 2a", "edited 3a" ) )

	editable.edit_lines( 1, 3, directions.RIGHT,
		( "edited 2b", "edited 3b", "edited 4b" ) )

	editable.edit_lines( 2, 4, directions.RIGHT,
		( "edited 3c", "edited 4c", "edited 5c" ) )

	# Ask for lines 1 to 4
	lines = editable.get_lines( 0, 4 )

	assert_strings_equal( lines[0].left, "line 1 here" )
	assert_strings_equal( lines[0].right, "edited 1a" )
	assert( lines[0].status == difflinetypes.DIFFERENT )
	assert( lines[0].left_edited == False )
	assert( lines[0].right_edited == True )

	assert_strings_equal( lines[1].left, "line 2 here" )
	assert_strings_equal( lines[1].right, "edited 2b" )
	assert( lines[1].status == difflinetypes.DIFFERENT )
	assert( lines[1].left_edited == False )
	assert( lines[1].right_edited == True )

	assert_strings_equal( lines[2].left, "line 3 here" )
	assert_strings_equal( lines[2].right, "edited 3c" )
	assert( lines[2].status == difflinetypes.DIFFERENT )
	assert( lines[2].left_edited == False )
	assert( lines[2].right_edited == True )

	assert_strings_equal( lines[3].left, "line 4 here" )
	assert_strings_equal( lines[3].right, "edited 4c" )
	assert( lines[3].status == difflinetypes.DIFFERENT )
	assert( lines[3].left_edited == False )
	assert( lines[3].right_edited == True )

	assert_lines_lists_equal( old_static_lines, staticdiffmodel.get_lines() )

def delete_line():
	staticdiffmodel = _make_static_diffmodel()
	old_static_lines = list( ln.clone() for ln in staticdiffmodel.get_lines() )

	editable = EditableDiffModel( staticdiffmodel )

	editable.delete_line( 1, directions.RIGHT )

	# Ask for lines 1 to 3
	lines = editable.get_lines( 0, 3 )

	ln = lines[0]
	assert_strings_equal( ln.left, "line 1 here" )
	assert_strings_equal( ln.right, "line 1 here" )
	assert( ln.status == difflinetypes.IDENTICAL )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )

	ln = lines[1]
	assert_strings_equal( ln.left, "line 2 here" )
	assert_strings_equal( ln.right, None )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == True )

	ln = lines[2]
	assert_strings_equal( ln.left, "line 3 here" )
	assert_strings_equal( ln.right, "line 3 here" )
	assert( ln.status == difflinetypes.IDENTICAL )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )

	assert_lines_lists_equal( old_static_lines, staticdiffmodel.get_lines() )

def edit_doesnt_change_anything():
	staticdiffmodel = _make_static_diffmodel()
	old_static_lines = list( ln.clone() for ln in staticdiffmodel.get_lines() )

	editable = EditableDiffModel( staticdiffmodel )

	# Make a change that actually doesn't change some lines
	editable.edit_lines( 0, 2, directions.LEFT,
		( "line 1 here", "edited 2", "line 3 here" ) )

	# Ask for lines 1 to 3
	lines = editable.get_lines( 0, 3 )

	assert_strings_equal( lines[0].left, "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here" )
	assert( lines[0].status == difflinetypes.IDENTICAL )
	assert( lines[0].left_edited == False )
	assert( lines[0].right_edited == False )

	assert_strings_equal( lines[1].left, "edited 2" )
	assert_strings_equal( lines[1].right, "line 2 here" )
	assert( lines[1].status == difflinetypes.DIFFERENT )
	assert( lines[1].left_edited == True )
	assert( lines[1].right_edited == False )

	assert_strings_equal( lines[2].left, "line 3 here" )
	assert_strings_equal( lines[2].right, "line 3 here" )
	assert( lines[2].status == difflinetypes.IDENTICAL )
	assert( lines[2].left_edited == False )
	assert( lines[2].right_edited == False )

	assert_lines_lists_equal( old_static_lines, staticdiffmodel.get_lines() )

class FakeFile( object ):
	def __init__( self ):
		self.txt = ""

	def write( self, towrite ):
		self.txt += towrite


def edit_after_delete():

	staticdiffmodel = _make_static_diffmodel()
	old_static_lines = list( ln.clone() for ln in staticdiffmodel.get_lines() )

	editable = EditableDiffModel( staticdiffmodel )

	# Delete then edit
	editable.delete_line( 1, directions.RIGHT )

	#editable.edit_lines( 2, 4, directions.RIGHT,
	#	( "edited 3c", "edited 4c", "edited 5c" ) )

	# Ask for lines 1 to 3
	lines = editable.get_lines( 0, 3 )

	ln = lines[0]
	assert_strings_equal( ln.left, "line 1 here" )
	assert_strings_equal( ln.right, "line 1 here" )
	assert( ln.status == difflinetypes.IDENTICAL )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )

	ln = lines[1]
	assert_strings_equal( ln.left, "line 2 here" )
	assert_strings_equal( ln.right, None )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == True )

	ln = lines[2]
	assert_strings_equal( ln.left, "line 3 here" )
	assert_strings_equal( ln.right, "line 3 here" )
	assert( ln.status == difflinetypes.IDENTICAL )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )

	assert_lines_lists_equal( old_static_lines, staticdiffmodel.get_lines() )

def delete_line_plus_edits():

	staticdiffmodel = _make_static_diffmodel()
	old_static_lines = list( ln.clone() for ln in staticdiffmodel.get_lines() )

	editable = EditableDiffModel( staticdiffmodel )

	# Make several overlapping changes, including a deletion
	editable.edit_lines( 0, 2, directions.RIGHT,
		( "edited 1a", "edited 2a", "edited 3a" ) )

	editable.edit_lines( 1, 3, directions.RIGHT,
		( "edited 2b", "edited 3b", "edited 4b" ) )

	editable.delete_line( 1, directions.RIGHT )

	editable.edit_lines( 2, 4, directions.RIGHT,
		( "edited 3c", "edited 4c", "edited 5c" ) )

	# Ask for lines 1 to 3
	lines = editable.get_lines( 0, 3 )

	ln = lines[0]
	assert_strings_equal( ln.left, "line 1 here" )
	assert_strings_equal( ln.right, "edited 1a" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == True )

	ln = lines[1]
	assert_strings_equal( ln.left, "line 2 here" )
	assert_strings_equal( ln.right, None )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == True )

	ln = lines[2]
	assert_strings_equal( ln.left, "line 3 here" )
	assert_strings_equal( ln.right, "edited 3c" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == True )

	assert_lines_lists_equal( old_static_lines, staticdiffmodel.get_lines() )

def write_to_file():
	fakefile = FakeFile()

	staticdiffmodel = _make_static_diffmodel()
	old_static_lines = list( ln.clone() for ln in staticdiffmodel.get_lines() )

	editable = EditableDiffModel( staticdiffmodel )

	# Make several overlapping changes, including a deletion
	editable.edit_lines( 0, 2, directions.RIGHT,
		( "edited 1a", "edited 2a", "edited 3a" ) )

	editable.edit_lines( 1, 3, directions.RIGHT,
		( "edited 2b", "edited 3b", "edited 4b" ) )

	editable.delete_line( 1, directions.RIGHT )

	editable.edit_lines( 2, 4, directions.RIGHT,
		( "edited 3c", "edited 4c", "edited 5c" ) )

	editable.write_to_file( fakefile, directions.RIGHT )

	assert_strings_equal( fakefile.txt,
		  "edited 1a\n"
		+ "edited 3c\n"
		+ "edited 4c\n"
		+ "edited 5c\n"
		+ "line 6 here\n"
		+ "line 7 here\n"
		+ "line 8 here\n"
		+ "line 9 here\n"
		+ "line 10 here\n"
		)

	assert_lines_lists_equal( old_static_lines, staticdiffmodel.get_lines() )

def write_to_file_no_changes():
	fakefile = FakeFile()

	staticdiffmodel = _make_static_diffmodel()
	editable = EditableDiffModel( staticdiffmodel )

	editable.write_to_file( fakefile, directions.LEFT )

	assert_strings_equal( fakefile.txt,
		  "line 1 here\n"
		+ "line 2 here\n"
		+ "line 3 here\n"
		+ "line 4 here\n"
		+ "line 5 here\n"
		+ "line 6 here\n"
		+ "line 7 here\n"
		+ "line 8 here\n"
		+ "line 9 here\n"
		+ "previous 10\n"
		)


def run():
	edit_line()
	edit_several_lines()
	edit_both_sides()
	delete_line()
	edit_starts_before()
	edit_ends_after()
	edit_spans_before_and_after()
	edit_doesnt_touch()
	several_edits()
	edit_after_delete()
	delete_line_plus_edits()
	edit_doesnt_change_anything()
	write_to_file()
	write_to_file_no_changes()

	#add_line() # TODO: requires us to shift all subsequent lines down

