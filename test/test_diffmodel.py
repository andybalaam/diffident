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

from asserts import assert_strings_equal

from lib.diffmodel import DiffModel
import lib.difflinetypes as difflinetypes

class FakeParser:
	def parse_lines( self, line_callback ):
		line_callback( "line 1\n", "line 1\n", difflinetypes.IDENTICAL )
		line_callback( "line 2 left\n", None, difflinetypes.REMOVE )
		line_callback( None, "line 3 right\n", difflinetypes.ADD )
		line_callback( "line 4 left\n", "line 4 right\n",
			difflinetypes.DIFFERENT )

def get_lines():
	parser = FakeParser()
	diffmodel = DiffModel( parser )
	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left, "line 1" )
	assert_strings_equal( lines[0].right, "line 1" )
	assert( lines[0].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[1].left, "line 2 left" )
	assert_strings_equal( lines[1].right, None )
	assert( lines[1].status == difflinetypes.REMOVE )

	assert_strings_equal( lines[2].left, None )
	assert_strings_equal( lines[2].right, "line 3 right" )
	assert( lines[2].status == difflinetypes.ADD )

	assert_strings_equal( lines[3].left, "line 4 left" )
	assert_strings_equal( lines[3].right, "line 4 right" )
	assert( lines[3].status == difflinetypes.DIFFERENT )

def run():
	get_lines()

