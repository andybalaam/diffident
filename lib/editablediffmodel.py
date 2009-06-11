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
		def __init__( self, first_line, side, new_strs ):
			self.first_line = first_line
			self.new_strs_len = len( new_strs )

			# TODO: don't repeat yourself here
			if side == directions.LEFT:
				self.lines = [ DiffLine( s, None, difflinetypes.DIFFERENT,
					True, False ) for s in new_strs ]
			else:
				self.lines = [ DiffLine( None, s, difflinetypes.DIFFERENT,
					False, True ) for s in new_strs ]

		def do_lines( self, start, end, lines_to_adjust,
				edit_num, save_points ):

			#print "lines_to_adjust =", lines_to_adjust
			#print start, self.first_line, end

			if start <= self.first_line < end:
				insert_point = self.first_line - start
				lines_to_adjust[ insert_point : insert_point ] = self.lines[:end-self.first_line]
			else:
				overlap = start - self.first_line
				if overlap > 0:
					lines_to_adjust[ 0 : 0 ] = self.lines[overlap:overlap+(end-start)]

		def do_single_line( self, line_num, ln, edit_num, save_points ):
			selfsta = self.first_line
			selfend = self.first_line + self.new_strs_len
			if selfsta <= line_num < selfend:
				return self.lines[ line_num - selfsta ]
			else:
				return ln

	class Edit( object ):
		def __init__( self, start_line, end_line, side, new_strs ):
			self.start_line = start_line
			self.end_line = end_line
			if side == directions.LEFT:
				self.get_side = lambda line: line.left
				self.set_side = self._set_left_side
				self.set_side_edited = self._set_left_side_edited
			else:
				self.get_side = lambda line: line.right
				self.set_side = self._set_right_side
				self.set_side_edited = self._set_right_side_edited
			self.side = side
			self.new_strs = new_strs

		def do_lines( self, start, end, lines_to_adjust,
				edit_num, save_points ):
			# If this edit is not relevant to the lines required, exit
			if end is not None and self.start_line >= end:
				return
			elif self.end_line <= start:
				return

			# Adjust our start and end point to be relative to the
			# start of this array of lines
			adj_sta = self.start_line - start
			adj_end = self.end_line - start

			# Get an iterator to the first affected line in the supplied
			# line array, and an iterator to the first relevant string in
			# this edit.
			toadj_iter = lines_to_adjust.__iter__()
			new_iter = self.new_strs.__iter__()

			# Skip forward in either the supplied array ...
			if adj_sta > 0:
				for i in xrange( adj_sta ):
					toadj_iter.next()
			elif adj_sta < 0: # ... or our list of edited lines
				for i in xrange( -adj_sta ):
					new_iter.next()

			# Make a list of the modifed lines
			lines_to_add = []
			try:
				for new_str in new_iter:
					oldline = toadj_iter.next()
					if self.get_side( oldline ) != new_str:
						newline = oldline.clone()
						self.adjust_line( newline, new_str, edit_num,
							save_points )
						lines_to_add.append( newline )
					else:
						lines_to_add.append( oldline )
			except StopIteration:
				pass # If we ran our of toadj_iter's, that means we
				     # have reached the end of the lines the user cares
				     # about, but this edit actually goes on beyond that.
				     # We stop here since the user doesn't care!

			# Replace the old lines with the modified ones
			if adj_sta < 0:
				adj_sta = 0
			end_of_slice = adj_sta + len( lines_to_add )
			lines_to_adjust[adj_sta:end_of_slice] = lines_to_add

		def adjust_line( self, toadj, new_str, edit_num, save_points ):
			self.set_side( toadj, new_str )
			if edit_num >= save_points[ self.side ]:
				self.set_side_edited( toadj )
			if toadj.left == toadj.right:
				toadj.status = difflinetypes.IDENTICAL
			else:
				toadj.status = difflinetypes.DIFFERENT

		def do_single_line( self, line_num, ln, edit_num, save_points ):
			if self.start_line <= line_num < self.end_line:
				relative_line_num = line_num - self.start_line
				ln = ln.clone()
				self.adjust_line( ln, self.new_strs[relative_line_num],
					edit_num, save_points )
			return ln

		def _set_left_side( self, line, strtoset ):
			line.left = strtoset

		def _set_left_side_edited( self, line ):
			line.left_edited = True

		def _set_right_side( self, line, strtoset ):
			line.right = strtoset

		def _set_right_side_edited( self, line ):
			line.right_edited = True

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

		# TODO: factor out and tidy
		staticstart = start
		staticend = end
		for edit in self.edits:
			if isinstance( edit, EditableDiffModel.Add ):
				if edit.first_line < staticstart:
					staticstart -= min( staticstart - edit.first_line,
						edit.new_strs_len )
				if staticend is not None and edit.first_line < staticend:
					staticend -= min( staticend - edit.first_line,
						edit.new_strs_len )

		lines = self.staticdiffmodel.get_lines( staticstart, staticend )

		for edit_num, edit in enumerate( self.edits ):
			edit.do_lines( start, end, lines, edit_num, self.save_points )

		return lines

	def get_line( self, line_num ):

		# TODO: factor out and tidy
		static_line_num = line_num
		for edit in self.edits:
			if ( isinstance( edit, EditableDiffModel.Add )
					and edit.first_line < static_line_num ):
				static_line_num -= min( static_line_num - edit.first_line,
					edit.new_strs_len )

		ln = self.staticdiffmodel.get_line( static_line_num )

		for edit_num, edit in enumerate( self.edits ):
			ln = edit.do_single_line( line_num, ln, edit_num, self.save_points )

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

		# If this edit changes anything, store it
		if self.existing_lines_different(
				first_line_num, last_line_num, side,  lines ):
			self.edits.append( EditableDiffModel.Edit(
				first_line_num, last_line_num, side, lines ) )

	def delete_lines( self, first_line_num, last_line_num, side ):
		num_nones = 1 + last_line_num - first_line_num
		nones = [ None ] * num_nones
		self.edits.append( EditableDiffModel.Edit(
			first_line_num, last_line_num, side, nones ) )

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
	
	def existing_lines_different( self, first_line_num, last_line_num,
			side, strs ):

		if side == directions.LEFT:
			get_side = lambda line: line.left
		else:
			get_side = lambda line: line.right

		existing_lines = self.get_lines( first_line_num, last_line_num )

		existing_strs = map( get_side, existing_lines )

		return ( existing_strs != strs )

