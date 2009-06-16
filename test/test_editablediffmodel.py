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
	assert( len( lines ) == 2 )

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
	assert( len( lines ) == 2 )

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
	assert( len( lines ) == 4 )

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
	assert( len( lines ) == 1 )

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
	assert( len( lines ) == 4 )

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

def delete_lines():
	staticdiffmodel = _make_static_diffmodel()
	old_static_lines = list( ln.clone() for ln in staticdiffmodel.get_lines() )

	editable = EditableDiffModel( staticdiffmodel )

	editable.delete_lines( 1, 2, directions.RIGHT )

	# Ask for lines 1 to 4
	lines = editable.get_lines( 0, 4 )
	assert( len( lines ) == 4 )

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
	assert_strings_equal( ln.right, None )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == True )

	ln = lines[3]
	assert_strings_equal( ln.left, "line 4 here" )
	assert_strings_equal( ln.right, "line 4 here" )
	assert( ln.status == difflinetypes.IDENTICAL )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )

	assert_lines_lists_equal( old_static_lines, staticdiffmodel.get_lines() )

def edit_doesnt_change_line():
	staticdiffmodel = _make_static_diffmodel()
	old_static_lines = list( ln.clone() for ln in staticdiffmodel.get_lines() )

	editable = EditableDiffModel( staticdiffmodel )

	# Make a change that actually doesn't change some lines
	editable.edit_lines( 0, 2, directions.LEFT,
		( "line 1 here", "edited 2", "line 3 here" ) )

	# Ask for lines 1 to 3
	lines = editable.get_lines( 0, 3 )
	assert( len( lines ) == 3 )

	assert_strings_equal( lines[0].left, "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here" )
	assert( lines[0].status == difflinetypes.IDENTICAL )
	assert( lines[0].left_edited == True ) # Because this is part of a real
	                                       # change, we do mark it as changed.
	                                       # This may be fixed in future
	assert( lines[0].right_edited == False )

	assert_strings_equal( lines[1].left, "edited 2" )
	assert_strings_equal( lines[1].right, "line 2 here" )
	assert( lines[1].status == difflinetypes.DIFFERENT )
	assert( lines[1].left_edited == True )
	assert( lines[1].right_edited == False )

	assert_strings_equal( lines[2].left, "line 3 here" )
	assert_strings_equal( lines[2].right, "line 3 here" )
	assert( lines[2].status == difflinetypes.IDENTICAL )
	assert( lines[2].left_edited == True ) # Because this is part of a real
	                                       # change, we do mark it as changed.
	                                       # This may be fixed in future
	assert( lines[2].right_edited == False )

	assert_lines_lists_equal( old_static_lines, staticdiffmodel.get_lines() )

def edit_doesnt_change_anything():
	staticdiffmodel = _make_static_diffmodel()
	old_static_lines = list( ln.clone() for ln in staticdiffmodel.get_lines() )

	editable = EditableDiffModel( staticdiffmodel )

	# Make a change that actually doesn't change any lines
	editable.edit_lines( 0, 2, directions.LEFT,
		[ "line 1 here", "line 2 here", "line 3 here" ] )

	# Ask for lines 1 to 3
	lines = editable.get_lines( 0, 3 )
	assert( len( lines ) == 3 )

	assert_strings_equal( lines[0].left, "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here" )
	assert( lines[0].status == difflinetypes.IDENTICAL )
	assert( lines[0].left_edited == False )
	assert( lines[0].right_edited == False )

	assert_strings_equal( lines[1].left, "line 2 here" )
	assert_strings_equal( lines[1].right, "line 2 here" )
	assert( lines[1].status == difflinetypes.IDENTICAL )
	assert( lines[1].left_edited == False )
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
	editable.delete_lines( 1, 1, directions.RIGHT )

	editable.edit_lines( 2, 4, directions.RIGHT,
		( "edited 3c", "edited 4c", "edited 5c" ) )

	# Ask for lines 1 to 3
	lines = editable.get_lines( 0, 3 )
	assert( len( lines ) == 3 )

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
	assert_strings_equal( ln.right, "edited 3c" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == True )

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

	editable.delete_lines( 1, 1, directions.RIGHT )

	editable.edit_lines( 2, 4, directions.RIGHT,
		( "edited 3c", "edited 4c", "edited 5c" ) )

	# Ask for lines 1 to 3
	lines = editable.get_lines( 0, 3 )
	assert( len( lines ) == 3 )

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

	editable.delete_lines( 1, 1, directions.RIGHT )

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

def add_lines_get_num_lines():
	"""The number of lines is correctly reported when lines have been added."""

	staticdiffmodel = _make_static_diffmodel()
	editable = EditableDiffModel( staticdiffmodel )

	assert( editable.get_num_lines() == 10 )

	editable.add_lines( 3, directions.LEFT,
		["new line 3a", "new line 3b", "new line 3c"] )

	assert( editable.get_num_lines() == 13 )

	editable.add_lines( 6, directions.LEFT, ["new line 4a", "new line 4b"] )
	editable.add_lines( 4, directions.LEFT, ["new line 3ai", "new line 3aii"] )

	assert( editable.get_num_lines() == 17 )

def add_lines_before():
	"""The lines before an add are unaffected by it."""

	staticdiffmodel = _make_static_diffmodel()
	editable = EditableDiffModel( staticdiffmodel )

	editable.add_lines( 3, directions.LEFT, ["new line 3a", "new line 3b"] )
	editable.add_lines( 6, directions.LEFT, ["new line 4a", "new line 4b"] )

	# Get some lines before the add
	lines = editable.get_lines( 0, 3 )
	assert( len( lines ) == 3 )

	ln = lines[0]
	assert_strings_equal( ln.left, "line 1 here" )
	assert_strings_equal( ln.right, "line 1 here" )
	assert( ln.status == difflinetypes.IDENTICAL )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )
	assert( ln == editable.get_line( 0 ) ) # Sanity for get_line

	ln = lines[1]
	assert_strings_equal( ln.left, "line 2 here" )
	assert_strings_equal( ln.right, "line 2 here" )
	assert( ln.status == difflinetypes.IDENTICAL )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )
	assert( ln == editable.get_line( 1 ) ) # Sanity for get_line

	ln = lines[2]
	assert_strings_equal( ln.left, "line 3 here" )
	assert_strings_equal( ln.right, "line 3 here" )
	assert( ln.status == difflinetypes.IDENTICAL )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )
	assert( ln == editable.get_line( 2 ) ) # Sanity for get_line

def add_lines_after():
	"""The lines after an add are shifted down."""

	staticdiffmodel = _make_static_diffmodel()
	editable = EditableDiffModel( staticdiffmodel )

	# TODO: change to this
	editable.add_lines( 3, directions.LEFT, ["new line 3a"] )
	editable.add_lines( 2, directions.LEFT, ["new line 2a", "new line 2b"] )

	# Get some lines after the add
	lines = editable.get_lines( 6, 8 )

	assert( len( lines ) == 2 )

	ln = lines[0]
	assert_strings_equal( ln.left, "line 4 here" )
	assert_strings_equal( ln.right, "line 4 here" )
	assert( ln.status == difflinetypes.IDENTICAL )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )
	assert( ln == editable.get_line( 6 ) ) # Sanity for get_line

	ln = lines[1]
	assert_strings_equal( ln.left, "line 5 here" )
	assert_strings_equal( ln.right, "line 5 here different" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )
	assert( ln == editable.get_line( 7 ) ) # Sanity for get_line

def add_lines_after_overlapping():
	"""The lines after an add are shifted down, even when the adds are overlapping."""

	staticdiffmodel = _make_static_diffmodel()
	editable = EditableDiffModel( staticdiffmodel )

	editable.add_lines( 2, directions.LEFT, ["new line 2a", "new line 2c"] )
	editable.add_lines( 3, directions.LEFT, ["new line 2b"] )

	# Get some lines after the add
	lines = editable.get_lines( 6, 8 )

	assert( len( lines ) == 2 )

	ln = lines[0]
	assert_strings_equal( ln.left, "line 4 here" )
	assert_strings_equal( ln.right, "line 4 here" )
	assert( ln.status == difflinetypes.IDENTICAL )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )
	assert( ln == editable.get_line( 6 ) ) # Sanity for get_line

	ln = lines[1]
	assert_strings_equal( ln.left, "line 5 here" )
	assert_strings_equal( ln.right, "line 5 here different" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )
	assert( ln == editable.get_line( 7 ) ) # Sanity for get_line

def add_lines_containing():
	"""The lines containing an add are calculated correctly."""

	staticdiffmodel = _make_static_diffmodel()
	editable = EditableDiffModel( staticdiffmodel )

	editable.add_lines( 3, directions.LEFT, ["new line 3a", "new line 3b"] )

	# Get some lines containing the add
	lines = editable.get_lines( 1, 6 )
	assert( len( lines ) == 5 )

	ln = lines[0]
	assert_strings_equal( ln.left, "line 2 here" )
	assert_strings_equal( ln.right, "line 2 here" )
	assert( ln.status == difflinetypes.IDENTICAL )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )
	assert( ln == editable.get_line( 1 ) ) # Sanity for get_line

	ln = lines[1]
	assert_strings_equal( ln.left, "line 3 here" )
	assert_strings_equal( ln.right, "line 3 here" )
	assert( ln.status == difflinetypes.IDENTICAL )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )
	assert( ln == editable.get_line( 2 ) ) # Sanity for get_line

	ln = lines[2]
	assert_strings_equal( ln.left, "new line 3a" )
	assert_strings_equal( ln.right, None )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == True )
	assert( ln.right_edited == False )
	assert( ln == editable.get_line( 3 ) ) # Sanity for get_line

	ln = lines[3]
	assert_strings_equal( ln.left, "new line 3b" )
	assert_strings_equal( ln.right, None )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == True )
	assert( ln.right_edited == False )
	assert( ln == editable.get_line( 4 ) ) # Sanity for get_line

	ln = lines[4]
	assert_strings_equal( ln.left, "line 4 here" )
	assert_strings_equal( ln.right, "line 4 here" )
	assert( ln.status == difflinetypes.IDENTICAL )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )
	assert( ln == editable.get_line( 5 ) ) # Sanity for get_line

def add_lines_overlapping_left():
	"""If an add overlaps the region we are asking for on the left,
	we still calculate the right answer."""

	staticdiffmodel = _make_static_diffmodel()
	editable = EditableDiffModel( staticdiffmodel )

	editable.add_lines( 3, directions.RIGHT,
		[
		"new line 3a",
		"new line 3b",
		"new line 3c",
		"new line 3d",
		] )

	# Get some lines containing the add
	lines = editable.get_lines( 5, 8 )
	assert( len( lines ) == 3 )

	ln = lines[0]
	assert_strings_equal( ln.left, None )
	assert_strings_equal( ln.right, "new line 3c" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == True )
	assert( ln == editable.get_line( 5 ) ) # Sanity for get_line

	ln = editable.get_line( 6 )
	assert_strings_equal( ln.left, None )
	assert_strings_equal( ln.right, "new line 3d" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == True )
	assert( ln == lines[1] ) # Sanity - get_lines gives same answer as get_line

	ln = lines[2]
	assert_strings_equal( ln.left, "line 4 here" )
	assert_strings_equal( ln.right, "line 4 here" )
	assert( ln.status == difflinetypes.IDENTICAL )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )
	assert( ln == editable.get_line( 7 ) ) # Sanity for get_line

def add_lines_overlapping_right():
	"""If an add overlaps the region we are asking for on the right,
	we still calculate the right answer."""

	staticdiffmodel = _make_static_diffmodel()
	editable = EditableDiffModel( staticdiffmodel )

	editable.add_lines( 1, directions.RIGHT,
		[
		"new line 1a",
		"new line 1b",
		"new line 1c",
		"new line 1d",
		] )

	# Get some lines containing the add
	lines = editable.get_lines( 0, 2 )
	assert( len( lines ) == 2 )

	ln = lines[0]
	assert_strings_equal( ln.left, "line 1 here" )
	assert_strings_equal( ln.right, "line 1 here" )
	assert( ln.status == difflinetypes.IDENTICAL )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )
	assert( ln == editable.get_line( 0 ) ) # Sanity for get_line

	ln = lines[1]
	assert_strings_equal( ln.left, None )
	assert_strings_equal( ln.right, "new line 1a" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == True )
	assert( ln == editable.get_line( 1 ) ) # Sanity for get_line

def add_lines_spanning():
	"""If an add overlaps the entire region we asking for,
	we still calculate the right answer."""

	staticdiffmodel = _make_static_diffmodel()
	editable = EditableDiffModel( staticdiffmodel )

	editable.add_lines( 1, directions.RIGHT,
		[
		"new line 1a",
		"new line 1b",
		"new line 1c",
		"new line 1d",
		] )

	# Get some lines containing the add
	lines = editable.get_lines( 2, 4 )
	assert( len( lines ) == 2 )

	ln = lines[0]
	assert_strings_equal( ln.left, None )
	assert_strings_equal( ln.right, "new line 1b" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == True )
	assert( ln == editable.get_line( 2 ) ) # Sanity for get_line

	ln = lines[1]
	assert_strings_equal( ln.left, None )
	assert_strings_equal( ln.right, "new line 1c" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == True )
	assert( ln == editable.get_line( 3 ) ) # Sanity for get_line

def add_inside_another_add():
	"""If an add lands inside another add,
	we still calculate the right answer."""

	staticdiffmodel = _make_static_diffmodel()
	editable = EditableDiffModel( staticdiffmodel )

	editable.add_lines( 1, directions.RIGHT,
		[
		"new line 1a",
		"new line 1b",
		"new line 1c",
		"new line 1d",
		] )

	editable.add_lines( 3, directions.LEFT,
		[
		"new line 1bi",
		"new line 1bii",
		] )

	# Get some lines containing the add
	lines = editable.get_lines( 0 , 8 )
	assert( len( lines ) == 8 )

	ln = lines[0]
	assert_strings_equal( ln.left, "line 1 here" )
	assert_strings_equal( ln.right, "line 1 here" )
	assert( ln == editable.get_line( 0 ) ) # Sanity for get_line

	ln = lines[1]
	assert_strings_equal( ln.left, None )
	assert_strings_equal( ln.right, "new line 1a" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == True )
	assert( ln == editable.get_line( 1 ) ) # Sanity for get_line

	ln = lines[2]
	assert_strings_equal( ln.left, None )
	assert_strings_equal( ln.right, "new line 1b" )
	assert( ln == editable.get_line( 2 ) ) # Sanity for get_line

	ln = lines[3]
	assert_strings_equal( ln.left, "new line 1bi" )
	assert_strings_equal( ln.right, None )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == True )
	assert( ln.right_edited == False )
	assert( ln == editable.get_line( 3 ) ) # Sanity for get_line

	ln = lines[4]
	assert_strings_equal( ln.left, "new line 1bii" )
	assert_strings_equal( ln.right, None )
	assert( ln == editable.get_line( 4 ) ) # Sanity for get_line

	ln = lines[5]
	assert_strings_equal( ln.left, None )
	assert_strings_equal( ln.right, "new line 1c" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == True )
	assert( ln == editable.get_line( 5 ) ) # Sanity for get_line

	ln = lines[6]
	assert_strings_equal( ln.left, None )
	assert_strings_equal( ln.right, "new line 1d" )
	assert( ln == editable.get_line( 6 ) ) # Sanity for get_line

	ln = lines[7]
	assert_strings_equal( ln.left, "line 2 here" )
	assert_strings_equal( ln.right, "line 2 here" )
	assert( ln == editable.get_line( 7 ) ) # Sanity for get_line

def several_edits_and_adds():
	assert( False )

def has_edit_affecting_side():

	staticdiffmodel = _make_static_diffmodel()
	editable = EditableDiffModel( staticdiffmodel )

	assert( not editable.has_edit_affecting_side( directions.RIGHT ) )
	assert( not editable.has_edit_affecting_side( directions.LEFT ) )

	editable.edit_lines( 0, 2, directions.RIGHT,
		( "edited 1a", "edited 2a", "edited 3a" ) )

	editable.edit_lines( 1, 3, directions.RIGHT,
		( "edited 2b", "edited 3b", "edited 4b" ) )

	assert( editable.has_edit_affecting_side( directions.RIGHT ) )
	assert( not editable.has_edit_affecting_side( directions.LEFT ) )

	editable.delete_lines( 1, 1, directions.LEFT )

	assert( editable.has_edit_affecting_side( directions.RIGHT ) )
	assert( editable.has_edit_affecting_side( directions.LEFT ) )

def has_edit_affecting_side_nullchange():

	staticdiffmodel = _make_static_diffmodel()
	editable = EditableDiffModel( staticdiffmodel )

	assert( not editable.has_edit_affecting_side( directions.RIGHT ) )
	assert( not editable.has_edit_affecting_side( directions.LEFT ) )

	editable.edit_lines( 0, 2, directions.RIGHT,
		[ "line 1 here", "line 2 here", "line 3 here" ] )

	editable.edit_lines( 1, 3, directions.RIGHT,
		[ "line 2 here", "line 3 here", "line 4 here" ] )

	assert( not editable.has_edit_affecting_side( directions.LEFT ) )
	assert( not editable.has_edit_affecting_side( directions.RIGHT ) )

def has_edit_affecting_side_after_save():

	staticdiffmodel = _make_static_diffmodel()
	editable = EditableDiffModel( staticdiffmodel )

	editable.edit_lines( 0, 2, directions.RIGHT,
		( "edited 1a", "edited 2a", "edited 3a" ) )

	editable.edit_lines( 0, 2, directions.LEFT,
		( "edited left 1a", "edited left 2a", "edited left 3a" ) )

	#TODO: editable.add_lines add some lines

	assert( editable.has_edit_affecting_side( directions.RIGHT ) )
	assert( editable.has_edit_affecting_side( directions.LEFT ) )

	lines = editable.get_lines( 0, 3 )
	assert( len( lines ) == 3 )

	ln = lines[0]
	assert_strings_equal( ln.left, "edited left 1a" )
	assert_strings_equal( ln.right, "edited 1a" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == True )
	assert( ln.right_edited == True )

	editable.set_save_point( directions.LEFT )

	lines = editable.get_lines( 0, 3 )
	assert( len( lines ) == 3 )

	ln = lines[0]
	assert_strings_equal( ln.left, "edited left 1a" )
	assert_strings_equal( ln.right, "edited 1a" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == True )

	assert( editable.has_edit_affecting_side( directions.RIGHT ) )
	assert( not editable.has_edit_affecting_side( directions.LEFT ) )

	editable.edit_lines( 0, 2, directions.RIGHT,
		( "edited 1b", "edited 2b", "edited 3b" ) )

	editable.set_save_point( directions.RIGHT )

	assert( not editable.has_edit_affecting_side( directions.RIGHT ) )
	assert( not editable.has_edit_affecting_side( directions.LEFT ) )

	lines = editable.get_lines( 0, 3 )
	assert( len( lines ) == 3 )

	ln = lines[0]
	assert_strings_equal( ln.left, "edited left 1a" )
	assert_strings_equal( ln.right, "edited 1b" )
	assert( ln.status == difflinetypes.DIFFERENT )
	assert( ln.left_edited == False )
	assert( ln.right_edited == False )

def get_lines_beyond_end():
	staticdiffmodel = _make_static_diffmodel()
	editable = EditableDiffModel( staticdiffmodel )

	editable.edit_lines( 0, 2, directions.RIGHT,
		( "edited 1b", "edited 2b", "edited 3b" ) )

	# We ask for many lines, but get only those that exist
	lines = editable.get_lines( 0, 100 )
	assert( len( lines ) == 10 )

def get_line_beyond_end():
	staticdiffmodel = _make_static_diffmodel()
	editable = EditableDiffModel( staticdiffmodel )

	editable.edit_lines( 0, 2, directions.RIGHT,
		( "edited 1b", "edited 2b", "edited 3b" ) )

	line = editable.get_line( 9 )
	assert( line is not None )

	# We ask for a line out of range and get None
	line = editable.get_line( 10 )
	assert( line is None )

def get_line_before_start():
	staticdiffmodel = _make_static_diffmodel()
	editable = EditableDiffModel( staticdiffmodel )

	editable.edit_lines( 2, 4, directions.RIGHT,
		( "edited 3b", "edited 3b", "edited 3c" ) )

	line = editable.get_line( 1 )
	assert( line is not None )

	# We ask for a line out of range and get None
	line = editable.get_line( -1 )
	assert( line is None )

def run():

	edit_line()
	edit_several_lines()
	edit_both_sides()
	delete_lines()
	edit_starts_before()
	edit_ends_after()
	edit_spans_before_and_after()
	edit_doesnt_touch()
	several_edits()
	edit_after_delete()
	delete_line_plus_edits()
	edit_doesnt_change_line()
	edit_doesnt_change_anything()
	write_to_file()
	write_to_file_no_changes()

	add_lines_get_num_lines()
	add_lines_before()
	add_lines_after_overlapping()
	add_lines_after()
	add_lines_containing()
	add_lines_overlapping_left()
	add_lines_overlapping_right()
	add_lines_spanning()
	# TODO: add_lines_ask_for_all()
	add_inside_another_add()
	# TODO: implement: several_edits_and_adds()
	# TODO: implement: add_lines_write_to_file()
	# TODO: implement: add_then_edit()

	has_edit_affecting_side()
	has_edit_affecting_side_nullchange()
	has_edit_affecting_side_after_save()

	get_line_beyond_end()
	get_lines_beyond_end()
	get_line_before_start()

