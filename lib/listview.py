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

import lib.difflinetypes as difflinetypes

def empty_if_none( line ):
	if line is None:
		return ""
	else:
		return line

class ListView:
	"""A simple view on a DiffModel that just lists all the lines in a file
	side by side."""

	def __init__( self, diffmodel ):
		self.diffmodel = diffmodel
		self.columns = 80

	def set_columns( self, columns ):
		self.columns = columns

	def get_string( self ):

		half_width = int( ( self.columns - 4 ) / 2 )

		ret = ""
		lines = self.diffmodel.get_lines()
		for line in lines:
			if line.status == difflinetypes.IDENTICAL:
				divider = "   "
			elif line.status == difflinetypes.DIFFERENT:
				divider = "|  "
			elif line.status == difflinetypes.ADD:
				divider = ">  "
			elif line.status == difflinetypes.REMOVE:
				divider = "<"
			else:
				raise Exception( "Unknown line type %d." % line.status )

			pattern = "%%-%ds %s%%s\n" % ( half_width, divider )
			ret += pattern % ( empty_if_none( line.left ),
				empty_if_none( line.right ) )
		return ret

