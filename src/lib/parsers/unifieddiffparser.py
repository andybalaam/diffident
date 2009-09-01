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

import re
from lib.misc.constants import difflinetypes

def is_x_line( line, x ):
	# TODO exclude only lines exactly matching the pattern for the beginning
	# of a hunk.
	return ( line[0] == x and not line.startswith( x * 3 ) )

def is_minus_line( line ):
	return is_x_line( line, "-" )

def is_plus_line( line ):
	return is_x_line( line, "+" )

class UnifiedDiffParser( object ):
	"""Parses a diff in unified format and supplies the result to
	a consumer (usually a DiffModel) by calling the supplied callback
	function for each line."""

	class CountingIter( object ):
		"""A wrapper around an iterator that keeps count of how many times
		next() has been called."""

		def __init__( self, iter_ ):
			self.iter_ = iter_
			self.num = 0

		def __iter__( self ):
			return self

		def next( self ):
			ans = self.iter_.next()
			self.num += 1
			return ans

		def next_no_throw( self ):
			"""Call next and swallow any StopIteration exception.  If such
			an exception was thrown, return None."""
			try:
				return self.next()
			except StopIteration:
				return None

	def __init__( self, left_file, diff ):
		self.left_file = left_file
		self.diff = diff

	hunk_line_re = re.compile( r"@@ -(\d+),\d+ \+\d+,\d+ @@" )
	def parse_hunk_line( self, line ):
		"""Examine the supplied line and return the first line of the left-hand
		file if this is a hunk line, or -1 otherwise."""

		m = UnifiedDiffParser.hunk_line_re.match( line )
		if m:
			return int( m.group( 1 ) )
		else:
			return -1

	def read_left_to_linenum( self, line_callback, linenum, left_iter ):
		"""Read from the left-hand file, calling back to say each line
		is identical, until we reach the specified line number."""

		while left_iter.num < linenum - 1:
			try:
				left_line = left_iter.next()
			except StopIteration:
				raise Exception(
					"Reached the end of the left file unexpectedly." )
			line_callback( left_line, left_line, difflinetypes.IDENTICAL )

	def read_left_to_end( self, line_callback, left_iter ):
		"""Read all the way to the end of the left file, calling back to
		say each line is identical."""

		while True:
			try:
				left_line = left_iter.next()
			except StopIteration:
				break
			line_callback( left_line, left_line, difflinetypes.IDENTICAL )

	def process_removed_lines( self, line_callback, left_lines ):
		"""Call back for each line in left_lines saying it was removed."""

		for left_line in left_lines:
			line_callback( left_line, None, difflinetypes.REMOVE )
		# Clear the list
		left_lines[:] = []

	def read_diff_to_end_of_hunk( self, line_callback, left_iter, diff_iter ):
		"""Understand a hunk of Unified Diff Format, calling back for
		identical, changed, added and removed lines as specified."""

		left_lines = []
		hunk_left_begin = -1
		while True:
			try:
				diff_line = diff_iter.next()
			except StopIteration, e:
				# This means we have reached the end of the diff.  Anything
				# that is left in left_lines must have been removed.
				self.process_removed_lines( line_callback, left_lines )
				# We re-raise the exception to let our caller know we have
				# finished reading the diff.
				raise e

			# Find out whether this line is the beginning of hunk
			hunk_left_begin = self.parse_hunk_line( diff_line )
			# If it is, we must stop because we have finsished with the
			# previous hunk
			if hunk_left_begin >= 0:
				break

			# Look for each type of line.  We maintain a list of lines
			# beginning with '-', called left_lines.  When we hit a '+'
			# we can cancel out a minus and make a DIFFERENT line, or if
			# there are no minuses this is an ADD line.
			# If we are left with any minuses we make them REMOVE lines.
			# Lines starting with ' ' are IDENTICAL lines.
			if is_minus_line( diff_line ):
				left_lines.append( diff_line[1:] )
				left_iter.next_no_throw()
			elif is_plus_line( diff_line ):
				if len( left_lines ) > 0:
					line_callback( left_lines[0], diff_line[1:],
						difflinetypes.DIFFERENT )
					left_lines = left_lines[1:]
				else:
					line_callback( None, diff_line[1:], difflinetypes.ADD )
			else: # TODO: is_space_line
				self.process_removed_lines( line_callback, left_lines )

				real_line = diff_line[1:]
				line_callback( real_line, real_line,
					difflinetypes.IDENTICAL )
				left_iter.next_no_throw()

		# This tells our caller that we found a new hunk line (we must have
		# done since the only alternative is that we hit the end of the diff
		# in which case we raised an exception), and what line number it said
		# the new hunk starts at (in the left file).
		return hunk_left_begin

	def parse_lines( self, line_callback ):
		"""Parse the diff supplied in the constructor.  For each line found,
		call the supplied line_callback function with three arguments:
		the line on the left (or None if this is an ADD),
		the line on the right (or None if this is a REMOVE),
		and the type of line (a constant from constants.difflinetypes)."""

		diff_iter = self.diff.__iter__()
		left_iter = UnifiedDiffParser.CountingIter( self.left_file.__iter__() )

		# Go through all lines in the diff, and if we find the beginning of
		# hunk, read from the left file up to that hunk (since the files are
		# identical where there is no hunk), then process the hunk, then
		# repeat.  At the end, read to the end of the left file.

		try:
			diff_line = diff_iter.next()
		except StopIteration:
			diff_line = None

		if diff_line is not None:
			hunk_left_begin = self.parse_hunk_line( diff_line )
			while True:
				# If this line was beginning a hunk, read the hunk
				if hunk_left_begin >= 0:
					self.read_left_to_linenum( line_callback, hunk_left_begin, left_iter )
					try:
						hunk_left_begin = self.read_diff_to_end_of_hunk(
							line_callback, left_iter, diff_iter )
					except StopIteration:
						break
				else:
					# Otherwise, go the next line and find out whether it is
					# the beginning of a hunk
					try:
						diff_line = diff_iter.next()
						hunk_left_begin = self.parse_hunk_line( diff_line )
					except StopIteration:
						break

		self.read_left_to_end( line_callback, left_iter )



