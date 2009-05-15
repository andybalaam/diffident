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

class DiffLine( object ):
	"""Abstract representation of a line in a diff."""

	def __init__( self, left, right, status ):
		"""Create a DiffLine.
		- left is the line in the left file, or
		  None if this is an ADD line.
		- right is the line in the right file, or
		  None if this is a REMOVE line.
		- status is a constant from lib.difflinetypes describing the type
		  of line this is: IDENTICAL, DIFFERENT, ADD or REMOVE."""

		self.left = left
		self.right = right
		self.status = status
		self.left_edited = False
		self.right_edited = False

	def __repr__( self ):
		if self.left_edited:
			led = "*"
		else:
			led = ""
		if self.right_edited:
			red = "*"
		else:
			red = ""
		return "%s%s -%s- %s%s" % ( self.left, led,
			self.status, self.right, red )

	def clone( self ):
		ret = DiffLine( self.left, self.right, self.status )
		ret.left_edited = self.left_edited
		ret.right_edited = self.right_edited

		return ret

