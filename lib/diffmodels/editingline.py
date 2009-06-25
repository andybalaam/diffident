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

from lib.misc.constants import difflinetypes
from lib.misc.constants import directions

from diffline import DiffLine

class EditingLine( DiffLine ):
	"""A container which accumulates edits to a line, and remembers
	the line number of the line being edited."""

	class NotEditedYet( object ):
		"""A dummy class indicating that one side of a DiffLine is
		missing. This will never compare equal with a string or None,
		which are what are normally stored in the DiffLine.left or
		right."""
		pass
	_NOT_EDITED_YET = NotEditedYet()

	def __init__( self, line_num ):

		DiffLine.__init__( self,
			EditingLine._NOT_EDITED_YET,
			EditingLine._NOT_EDITED_YET,
			difflinetypes.IDENTICAL )

		self.line_num = line_num

	def maybe_set_side( self, side, value, edited ):
		if side == directions.LEFT:
			if self.left == EditingLine._NOT_EDITED_YET:
				self.left = value
				self.left_edited = edited
				self._calc_properties()
		else:
			if ( self.right == EditingLine._NOT_EDITED_YET ):
				self.right = value
				self.right_edited = edited
				self._calc_properties()

	def _calc_properties( self ):
		if self.left == self.right:
			self.status = difflinetypes.IDENTICAL
		else:
			self.status = difflinetypes.DIFFERENT

	def is_fully_edited( self ):
		return EditingLine._NOT_EDITED_YET not in (
			self.left, self.right )

	def create_filled_in_diffline( self, staticdiffmodel ):
		"""If any parts of this line have not yet been affected by
		an edit, absorb them from the supplied static line and
		return a DiffLine object representing the final version
		of this line."""

		if not self.is_fully_edited():

			static_line = staticdiffmodel.get_line( self.line_num )

			if static_line is None:
				left = None
				right = None
			else:
				left = static_line.left
				right = static_line.right

			self.maybe_set_side( directions.LEFT,  left,  False )
			self.maybe_set_side( directions.RIGHT, right, False )

		return DiffLine.clone( self )


