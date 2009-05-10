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

from lib.constants import difflinetypes
from lib.constants import directions

class EditableDiffModel( object ):
	"""An abstract model of an editable set of differences between 2 files."""

	class Edit( object ):
		def __init__( self, start_line, end_line, side, new_strs ):
			self.start_line = start_line
			self.end_line = end_line
			if side == directions.LEFT:
				self.set_side = self._set_left_side
				self.other_side_edited = difflinetypes.EDITED_RIGHT
				self.this_side_edited  = difflinetypes.EDITED_LEFT
			else:
				self.set_side = self._set_right_side
				self.other_side_edited = difflinetypes.EDITED_LEFT
				self.this_side_edited  = difflinetypes.EDITED_RIGHT
			self.side = side
			self.new_strs = new_strs

		def do_lines( self, start, end, lines_to_adjust ):
			# If this edit is relevant to the lines required
			if end is not None and self.start_line >= end:
				return
			elif self.end_line <= start:
				return

			adj_sta = self.start_line - start
			adj_end = self.end_line - start

			toadj_iter = lines_to_adjust.__iter__()
			new_iter = self.new_strs.__iter__()

			start_pt = self.start_line - start
			if start_pt > 0:
				for i in xrange( start_pt ):
					toadj_iter.next()
			elif start_pt < 0:
				for i in xrange( -start_pt ):
					new_iter.next()

			try:
				for new_str in new_iter:
					toadj = toadj_iter.next()
					self.adjust_line( toadj, new_str )
			except StopIteration:
				pass # If we ran our of toadj_iter's, that means we
				     # have reached the end of the lines the user cares
				     # about, but this edit actually goes on beyond that.
				     # We stop here since the user doesn't care!

		def adjust_line( self, toadj, new_str ):
			self.set_side( toadj, new_str )
			if toadj.status == self.other_side_edited:
				toadj.status = difflinetypes.EDITED_BOTH
			else:
				toadj.status = self.this_side_edited

		def do_single_line( self, line_num, ln ):
			if self.start_line <= line_num < self.end_line:
				relative_line_num = line_num - self.start_line
				self.adjust_line( ln, self.new_strs[relative_line_num] )

		def _set_left_side( self, line, strtoset ):
			line.left = strtoset

		def _set_right_side( self, line, strtoset ):
			line.right = strtoset

	def __init__( self, staticdiffmodel ):
		self.staticdiffmodel = staticdiffmodel
		self.edits = []

	# DiffModel public functions:

	def get_lines( self, start=0, end=None ):
		lines = self.staticdiffmodel.get_lines( start, end )

		for edit in self.edits:
			edit.do_lines( start, end, lines )

		return lines

	def get_line( self, line_num ):
		ln = self.staticdiffmodel.get_line( line_num )
		for edit in self.edits:
			edit.do_single_line( line_num, ln )
		return ln

	def get_num_lines( self ):
		return self.staticdiffmodel.get_num_lines()

	# Our own public functions

	def edit_lines( self, first_line_num, last_line_num, side, lines ):
		"""Modify the lines specified by replacing them with the lines
		supplied.
		Note that last_line_num IS included in the range, and it is allowed
		to be smaller than first_line_num.
		side should be directions.LEFT or RIGHT.
		lines should be iterable and len()-able"""

		# Assure ourselves first is less than last
		if first_line_num > last_line_num:
			first_line_num, last_line_num = last_line_num, first_line_num

		# Change this into a standard range - the last line is not included
		last_line_num += 1

		assert( len( lines ) == ( last_line_num - first_line_num ) )

		self.edits.append( EditableDiffModel.Edit(
			first_line_num, last_line_num, side, lines ) )

	def delete_line( self, line_num, side ):
		self.edits.append( EditableDiffModel.Edit(
			line_num, line_num, side, ( None, ) ) )

