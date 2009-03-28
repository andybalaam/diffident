import re

def is_x_line( line, x ):
	return ( line[0] == x and not line.startswith( x * 3 ) )

def is_minus_line( line ):
	return is_x_line( line, "-" )

def is_plus_line( line ):
	return is_x_line( line, "+" )

class DiffModel:

	DIFFERENT = 0
	IDENTICAL = 1
	ADD       = 2
	REMOVE    = 3

	class DiffLine:
		def __init__( self, left, right, status ):
			self.left = left
			self.right = right
			self.status = status
		def __repr__( self ):
			return self.left + " -- " +  self.right

	class CountingIter:
		"""A wrapper around an iterator that keeps count of how many times
		next() has been called"""

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
			try:
				return self.next()
			except StopIteration:
				return None

	def __init__( self, left_file, right_file, diff ):
		self.left_file = left_file
		self.right_file = right_file
		self.diff = diff

	hunk_line_re = re.compile( r"@@ -(\d+),\d+ \+\d+,\d+ @@" )
	def parse_hunk_line( self, line ):
		"""Examine the supplied line and return the first line of the left-hand
		file if this is a hunk line, or -1 otherwise."""

		m = DiffModel.hunk_line_re.match( line )
		if m:
			return int( m.group( 1 ) )
		else:
			return -1

	def read_left_to_linenum( self, ret, linenum, left_iter ):
		while left_iter.num < linenum - 1:
			try:
				left_line = left_iter.next()
			except StopIteration:
				raise Exception(
					"Reached the end of the left file unexpectedly." )
			ret.append( DiffModel.DiffLine( left_line, left_line,
				DiffModel.IDENTICAL ) )

	def read_left_to_end( self, ret, left_iter ):
		while True:
			try:
				left_line = left_iter.next()
			except StopIteration:
				break
			ret.append( DiffModel.DiffLine( left_line, left_line,
				DiffModel.IDENTICAL ) )

	def read_diff_to_end_of_hunk( self, ret, left_iter, diff_iter ):
		left_lines = []
		hunk_left_begin = -1
		while True:
			# If this throws we allow the StopIteration exception to escape
			# to our caller.
			diff_line = diff_iter.next()

			hunk_left_begin = self.parse_hunk_line( diff_line )
			if hunk_left_begin > 0:
				break

			if is_minus_line( diff_line ):
				left_lines.append( diff_line[1:] )
				left_iter.next_no_throw()
			elif is_plus_line( diff_line ):
				ret.append( DiffModel.DiffLine( left_lines[0], diff_line[1:],
					DiffModel.DIFFERENT ) )
				left_lines = left_lines[1:]
			else:
				real_line = diff_line[1:]
				ret.append( DiffModel.DiffLine( real_line, real_line,
					DiffModel.IDENTICAL ) )
				left_iter.next_no_throw()

		# This will fail when we consider diffs expressing deletions
		assert( len( left_lines ) == 0 )

		return hunk_left_begin

	def get_lines( self ):
		ret = []

		diff_iter = self.diff.__iter__()
		left_iter = DiffModel.CountingIter( self.left_file.__iter__() )

		try:
			diff_line = diff_iter.next()
		except StopIteration:
			diff_line = None

		if diff_line is not None:
			hunk_left_begin = self.parse_hunk_line( diff_line )
			while True:
				if hunk_left_begin > 0:
					self.read_left_to_linenum( ret, hunk_left_begin, left_iter )
					try:
						hunk_left_begin = self.read_diff_to_end_of_hunk(
							ret, left_iter, diff_iter )
					except StopIteration:
						break
				else:
					try:
						diff_line = diff_iter.next()
						hunk_left_begin = self.parse_hunk_line( diff_line )
					except StopIteration:
						break

		self.read_left_to_end( ret, left_iter )

		return ret


