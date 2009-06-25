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


class ChangeEdit( object ):
	def __init__( self, start_line, end_line, side, new_strs ):
		self.start_line = start_line
		self.end_line = end_line
		self.num_added_lines = 0
		self.side = side
		self.new_strs = new_strs

		assert( len( new_strs ) == ( end_line - start_line ) )

	# TODO: combine with Add's impl
	def apply_to( self, annotated_lines, edit_num, save_points ):

		first_editable_line = None
		for ln in annotated_lines:
			if not ln.is_fully_edited():
				first_editable_line = ln.line_num
				break

		assert( first_editable_line is not None )

		if self.end_line <= first_editable_line:
			return True

		any_gaps_left = False
		for array_index, line in enumerate( annotated_lines ):
			if self.start_line <= line.line_num < self.end_line:
				if not line.is_fully_edited():
					new_str = self.new_strs[line.line_num -
						self.start_line]
					after_save = ( edit_num >= save_points[self.side] )
					modified = line.maybe_set_side( self.side, new_str,
						after_save )

			if not any_gaps_left:
				any_gaps_left = not line.is_fully_edited()

		return any_gaps_left

