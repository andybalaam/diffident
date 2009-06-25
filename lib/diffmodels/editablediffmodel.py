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

from lib.misc.constants import directions
from lib.misc import diffidenttools

from edit import Edit
from editingline import EditingLine

FILE_WRITING_CHUNK_SIZE = 1000  # When we write to file we use blocks this size

class EditableDiffModel( object ):
	"""An abstract model of an editable set of differences between 2 files."""

	def __init__( self, staticdiffmodel ):
		self.staticdiffmodel = staticdiffmodel
		self.edits = []
		self.num_added_lines = 0

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

		# TODO: Call something like self.staticdiffmodel.is_before_end( end ).
		#       This can return early in most cases, meaning we don't need to
		#       wait for diff to diff the whole model.
		num_lines = self.get_num_lines()
		if end is None or end > num_lines:
			end = num_lines

		# Create an array to hold the results.  This array starts off containing
		# ints to indicate which line number should be inserted in which place,
		# and as edits are found for each line number, the ints are replaced
		# with DiffLine objects.
		annotated_lines = list( EditingLine( line_num )
			for line_num in xrange( start, end ) )

		# Loop through all edits in reverse order, noting the
		# edit number (so that we can decide which edits should cause
		# an "edited" flag to be set), and applying them to the
		# list of lines we have made.
		for edit_num, edit in diffidenttools.reversed_enumerate( self.edits ):

			any_gaps_left = edit.apply_to( annotated_lines, edit_num,
				self.save_points )

			if not any_gaps_left:
				break

		ret = list( edited_line.create_filled_in_diffline(
			self.staticdiffmodel ) for edited_line in annotated_lines )

		return ret


	def get_line( self, line_num ):
		# TODO: Call something like staticdiffmodel.is_before_end( line_num ).
		#       This can return early in most cases, meaning we don't need to
		#       wait for diff to diff the whole model.
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
		return self.staticdiffmodel.get_num_lines() + self.num_added_lines

	# Our own public functions

	def edit_lines( self, first_line_num, last_line_num, side, lines ):
		"""Modify the lines specified by replacing them with the lines
		supplied.
		Note that last_line_num IS included in the range, and it is allowed
		to be smaller than first_line_num.
		side should be directions.LEFT or RIGHT.
		lines should be iterable and len()-able"""

		first_line_num, last_line_num = self._standard_range(
			first_line_num, last_line_num )

		assert( len( lines ) == ( last_line_num - first_line_num ) )

		# If this edit changes anything, store it
		if self._existing_lines_different( first_line_num, last_line_num,
				side,  lines ):
			edit = Edit( first_line_num, side, lines, is_add=False )
			self.edits.append( edit )

	def delete_lines( self, first_line_num, last_line_num, side ):
		"""Delete the lines specified and replace them with empty lines.
		Note that last_line_num IS included in the range, and it is allowed
		to be smaller than first_line_num.
		side should be directions.LEFT or RIGHT."""

		# We implement this by simply doing an edit that sets the lines
		# to None.

		first_line_num, last_line_num = self._standard_range(
			first_line_num, last_line_num )

		num_nones = last_line_num - first_line_num
		nones = [ None ] * num_nones

		edit = Edit( first_line_num, side, nones, is_add=False )
		self.edits.append( edit )

	def add_lines( self, before_line_num, side, strs ):
		"""Insert the lines supplied before the line specified.
		side should be directions.LEFT or RIGHT."""

		add = Edit( before_line_num, side, strs, is_add=True )
		self.edits.append( add )
		self.num_added_lines += add.num_added_lines

	def write_to_file( self, fl, side ):
		# We write this many lines at a time
		chunk_size = FILE_WRITING_CHUNK_SIZE

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

	def _standard_range( self, first, last ):
		# Assure ourselves first is <= than last
		if first > last:
			first, last = last, first

		# Change this into a standard range - the last line was not included
		last += 1

		return ( first, last )

	def _existing_lines_different( self, first_line_num, last_line_num,
			side, strs ):
		# NOTE: If this is slow, the UI can probably perform this check for us.
		#       It should be ok though because it only operates on the
		#       visible set of lines, not all of them.

		if side == directions.LEFT:
			get_side = lambda line: line.left
		else:
			get_side = lambda line: line.right

		existing_lines = self.get_lines( first_line_num, last_line_num )

		existing_strs = map( get_side, existing_lines )

		return ( existing_strs != strs )

