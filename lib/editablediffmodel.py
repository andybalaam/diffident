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

import itertools

from diffline import DiffLine

from lib.constants import difflinetypes
from lib.constants import directions

class EditableDiffModel( object ):
	"""An abstract model of an editable set of differences between 2 files."""

	class Add( object ):
		def __init__( self, start_line, side, new_strs ):
			self.start_line = start_line
			self.num_added_lines = len( new_strs )
			self.end_line = start_line + self.num_added_lines

			# TODO: don't repeat yourself here
			if side == directions.LEFT:
				self.lines = [ DiffLine( s, None, difflinetypes.DIFFERENT,
					True, False ) for s in new_strs ]
			else:
				self.lines = [ DiffLine( None, s, difflinetypes.DIFFERENT,
					False, True ) for s in new_strs ]

		def apply_to( self, annotated_lines, edit_num, save_points ):

			reduce_line_num_by = 0

			first_annotated_line = None
			for ln in annotated_lines:
				if ln.__class__ == int:
					first_annotated_line = ln
					break
				elif not ln.is_fully_edited():
					first_annotated_line = ln.line_num
					break

			assert( first_annotated_line is not None )

			if self.start_line < first_annotated_line:
				reduce_line_num_by += min(
					first_annotated_line - self.start_line,
					self.num_added_lines )

			any_gaps_left = False
			for array_index, line_num in enumerate( annotated_lines ):
				# We only process ints - if this is not an int, it is a line
				# that we have already modified.
				if line_num.__class__ == int:
					if self.start_line <= line_num < self.end_line:
						# TODO: can we avoid an array lookup by using an
						#       iterator?
						annotated_lines[array_index] = (
							self.lines[line_num - self.start_line] )
						reduce_line_num_by += 1
					else:
						any_gaps_left = True
						annotated_lines[array_index] -= reduce_line_num_by

			return any_gaps_left

	class Edit( object ):
		def __init__( self, start_line, end_line, side, new_strs ):
			self.start_line = start_line
			self.end_line = end_line
			self.num_added_lines = 0
			self.side = side
			self.new_strs = new_strs

			assert( len( new_strs ) == ( end_line - start_line ) )

		# TODO: combine with Add's impl
		def apply_to( self, annotated_lines, edit_num, save_points ):

			first_annotated_line = None
			for ln in annotated_lines:
				if ln.__class__ == int:
					first_annotated_line = ln
					break
				elif not ln.is_fully_edited():
					first_annotated_line = ln.line_num
					break

			assert( first_annotated_line is not None )

			if self.end_line <= first_annotated_line:
				return True

			any_gaps_left = False
			for array_index, line in enumerate( annotated_lines ):
				# We only process ints - if this is not an int, it is a line
				# that we have already modified.
				if line.__class__ == int:
					any_gaps_left = True
					if self.start_line <= line < self.end_line:
						# TODO: can we avoid an array lookup by using an
						#       iterator?
						
						after_save = ( edit_num >= save_points[self.side] )

						editcol = EditableDiffModel.EditingLine( line )
						editcol.maybe_set_side( self.side,
							self.new_strs[line - self.start_line], after_save )
						annotated_lines[array_index] = editcol
				else:
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

	def __init__( self, staticdiffmodel ):
		self.staticdiffmodel = staticdiffmodel
		self.edits = []

		# Save points are the array index of the edit on which
		# we saved the file.
		self.save_points = {
			directions.LEFT : 0,
			directions.RIGHT : 0,
			}

	# DiffModel public functions:

	def get_lines( self, start=0, end=None ):

		# Special case optimisation for if we have no edits at all
		if len( self.edits ) == 0:
			return self.staticdiffmodel.get_lines( start, end )

		num_lines = self.get_num_lines()
		if end is None or end > num_lines:
			end = num_lines

		# Create an array to hold the results.  This array starts off containing
		# ints to indicate which line number should be inserted in which place,
		# and as edits are found for each line number, the ints are replaced
		# with DiffLine objects.
		annotated_lines = list( xrange( start, end ) )

		# TODO: make a nice iterator for this loop?
		# Loop through all edits in reverse order, working out the
		# edit number (so that we can decide which edits should cause
		# an "edited" flag to be set), and applying them to the
		# list of lines we have made.
		for r_edit_num, edit in enumerate( reversed( self.edits ) ):
			edit_num = len( self.edits ) - r_edit_num - 1

			any_gaps_left = edit.apply_to( annotated_lines, edit_num,
				self.save_points )

			if not any_gaps_left:
				break

		ret = list( self._get_static_or_edited_line( edited_line )
			for edited_line in annotated_lines )

		return ret


	def get_line( self, line_num ):
		num_lines = self.get_num_lines()
		if line_num >= num_lines or line_num < 0:
			return None
		else:
			lines = self.get_lines( line_num, line_num + 1 )
			if len( lines ) != 1:
				raise Exception(
					"%d resulted in %d lines!" % ( line_num, len( lines ) ) )
			return lines[0]

	def get_num_lines( self ):
		# TODO: cache this value

		num_lines = self.staticdiffmodel.get_num_lines()

		for edit in self.edits:
			num_lines += edit.num_added_lines

		return num_lines

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

		# If this edit changes anything, store it
		if self._existing_lines_different(
				first_line_num, last_line_num, side,  lines ):
			self.edits.append( EditableDiffModel.Edit(
				first_line_num, last_line_num, side, lines ) )

	def delete_lines( self, first_line_num, last_line_num, side ):
		num_nones = 1 + last_line_num - first_line_num
		nones = [ None ] * num_nones
		self.edits.append( EditableDiffModel.Edit(
			first_line_num, last_line_num + 1, side, nones ) )

	def add_lines( self, before_line_num, side, strs ):
		self.edits.append( EditableDiffModel.Add( before_line_num, side,
			strs ) )

	def write_to_file( self, fl, side ):
		# We write this many lines at a time
		chunk_size = 1000

		num_lines = self.get_num_lines()
		next_lnum = 0
		prev_lnum = 0

		while next_lnum < num_lines:
			next_lnum += chunk_size
			if next_lnum > num_lines:
				next_lnum = num_lines

			lines = self.get_lines( prev_lnum, next_lnum )

			for line in lines:

				if side == directions.LEFT:
					towrite = line.left
				else:
					towrite = line.right

				if towrite is not None:
					towrite += "\n"
					fl.write( towrite )

			prev_lnum = next_lnum

	def has_edit_affecting_side( self, side ):

		for edit in itertools.islice( self.edits,
				self.save_points[side], None ):
			if edit.side == side:
				return True

		return False

	def set_save_point( self, side ):
		self.save_points[side] = len( self.edits )

	# Private functions
	
	def _existing_lines_different( self, first_line_num, last_line_num,
			side, strs ):
		# TODO: If this is slow, the UI can probably perform this check for us.
		#       It should be ok though because it only operates on the
		#       visible set of lines, not all of them.

		if side == directions.LEFT:
			get_side = lambda line: line.left
		else:
			get_side = lambda line: line.right

		existing_lines = self.get_lines( first_line_num, last_line_num )

		existing_strs = map( get_side, existing_lines )

		return ( existing_strs != strs )

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
				EditableDiffModel.EditingLine._NOT_EDITED_YET,
				EditableDiffModel.EditingLine._NOT_EDITED_YET,
				difflinetypes.IDENTICAL )

			self.line_num = line_num

		def maybe_set_side( self, side, value, edited ):
			if side == directions.LEFT:
				if self.left == EditableDiffModel.EditingLine._NOT_EDITED_YET:
					self.left = value
					self.left_edited = edited
					self._calc_properties()
					return True
			else:
				if ( self.right ==
						EditableDiffModel.EditingLine._NOT_EDITED_YET ):
					self.right = value
					self.right_edited = edited
					self._calc_properties()
					return True
			return False

		def _calc_properties( self ):
			if self.left == self.right:
				self.status = difflinetypes.IDENTICAL
			else:
				self.status = difflinetypes.DIFFERENT

		def is_fully_edited( self ):
			return EditableDiffModel.EditingLine._NOT_EDITED_YET not in (
				self.left, self.right )

		def create_filled_in_diffline( self, static_line ):
			"""If any parts of this line have not yet been affected by
			an edit, absorb them from the supplied static line and
			return a DiffLine object representing the final version
			of this line."""

			self.maybe_set_side( directions.LEFT,  static_line.left,  False )
			self.maybe_set_side( directions.RIGHT, static_line.right, False )

			return DiffLine.clone( self )


	def _get_static_or_edited_line( self, edited_line ):
		"""If edited_line is an int, return that line number from our static
		DiffModel.  Otherwise, we assume it is a DiffLine, and return it."""

		if edited_line.__class__ == int:
			# If it's an int it means return this line from the static model
			return self.staticdiffmodel.get_line( edited_line )
		elif edited_line.__class__ == DiffLine:
			# Adds put an object of the exact type we need into the array,
			# so we can just return it
			return edited_line
		else:
			# Otherwise it must be an EditingLine and we use that to
			# create the line to return

			static_line = self.staticdiffmodel.get_line( edited_line.line_num )
			return edited_line.create_filled_in_diffline( static_line )


