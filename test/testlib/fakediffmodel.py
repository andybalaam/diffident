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

class FakeDiffModel:
	def __init__( self ):
		self.lines = []

	def get_lines( self, start=0, end=None ):
		if end is None:
			return self.lines[start:]
		else:
			return self.lines[start:end]

	def get_line( self, line_num ):
		if 0 <= line_num < len( self.lines ):
			return self.lines[line_num]
		else:
			return None

	def get_num_lines( self ):
		return len( self.lines )

