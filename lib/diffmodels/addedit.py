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

from lib.misc.constants import directions

class AddEdit( object ):
	# TODO: combine common parts with Edit
	def __init__( self, start_line, side, new_strs ):
		self.start_line = start_line
		self.num_added_lines = len( new_strs )
		self.end_line = start_line + self.num_added_lines
		self.new_strs = new_strs
		self.side = side

	def _update_editing_line( self, line, line_num, edit_num, save_points ):
		after_save = ( edit_num >= save_points[self.side] )
		line.maybe_set_side( self.side,
			self.new_strs[line_num - self.start_line], after_save )
		line.maybe_set_side(
			directions.opposite_lr( self.side ), None, False )

	def apply_to( self, annotated_lines, edit_num, save_points ):
		reduce_line_num_by = 0

		first_editable_line = None
		for ln in annotated_lines:
			if not ln.is_fully_edited():
				first_editable_line = ln.line_num
				break

		assert( first_editable_line is not None )

		if self.start_line < first_editable_line:
			reduce_line_num_by += min(
				first_editable_line - self.start_line,
				self.num_added_lines )

		any_gaps_left = False
		for array_index, line in enumerate( annotated_lines ):
			if ( self.start_line <= line.line_num < self.end_line and
					not line.is_fully_edited() ):
				# This line is affected by this Add
				self._update_editing_line( line, line.line_num,
					edit_num, save_points )

				reduce_line_num_by += 1
			else:
				line.line_num -= reduce_line_num_by

			if not any_gaps_left:
				any_gaps_left = not line.is_fully_edited()

		return any_gaps_left
