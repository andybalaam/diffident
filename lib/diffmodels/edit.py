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

class Edit( object ):
	def __init__( self, start_line, side, new_strs, is_add ):
		self.is_add = is_add
		self.start_line = start_line
		self.side = side
		self.new_strs = new_strs

		if self.is_add:
			self.num_added_lines = len( new_strs )
			self.end_line = start_line + self.num_added_lines
		else:
			self.num_added_lines = 0
			self.end_line = start_line + len( new_strs )
		

	def update_editing_line( self, line, line_num, edit_num, save_points ):
		after_save = ( edit_num >= save_points[self.side] )
		line.maybe_set_side( self.side,
			self.new_strs[line_num - self.start_line], after_save )

		# If this is an add, the other side is None.  If not, it could
		# be affected by an earlier edit.
		if self.is_add:
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

		# If we're not adding (so not playing with line numbers), we can
		# exit early if we don't cross over with any editable lines
		if not self.is_add and self.end_line <= first_editable_line:
			return True

		# If we're an add we may have added some lines before the first
		# line we get to, so we must correct all the line numbers to
		# reflect this - we do this using "reduce_line_num_by"
		if self.is_add and self.start_line < first_editable_line:
			reduce_line_num_by += min(
				first_editable_line - self.start_line,
				self.num_added_lines )

		any_gaps_left = False
		for array_index, line in enumerate( annotated_lines ):
			if ( self.start_line <= line.line_num < self.end_line and
					not line.is_fully_edited() ):
				# This line is affected by this Edit
				self.update_editing_line( line, line.line_num,
					edit_num, save_points )

				# This line has been added, so later lines need to reduce
				# thier number by 1
				if self.is_add:
					reduce_line_num_by += 1
			else:
				# Reduce the current line number by the required amount.
				# This will always do nothing unless this is an add:
				assert( self.is_add or ( reduce_line_num_by == 0 ) )

				line.line_num -= reduce_line_num_by

			if not any_gaps_left:
				any_gaps_left = not line.is_fully_edited()

		return any_gaps_left

