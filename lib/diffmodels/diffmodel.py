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

from diffline import DiffLine

def strip_newline( line ):
	if line is not None and len( line ) > 0 and line[-1] == "\n":
		return line[:-1]
	else:
		return line

class DiffModel( object ):
	"""An abstract model of the differences between 2 files."""

	def __init__( self, parser ):
		self.parser = parser
		self.lines = None

	# Public functions

	def get_lines( self, start=0, end=None ):
		self.parse_if_needed()
		return self.lines[start:end]

	def get_line( self, line_num ):
		self.parse_if_needed()
		if 0 <= line_num < len( self.lines ):
			return self.lines[line_num]
		else:
			return None

	def get_num_lines( self ):
		self.parse_if_needed()
		return len( self.lines )

	# Private (ish) functions

	def parse_if_needed( self ):
		if self.lines is None:
			self.lines = []
			self.parser.parse_lines( self.line_callback )

	def line_callback( self, left, right, status ):
		"""Receive a callback from the parser saying that we have received a
		line."""
		self.lines.append( DiffLine( strip_newline( left ),
			strip_newline( right ), status ) )

