
def strip_newline( line ):
	if line is not None and len( line ) > 0 and line[-1] == "\n":
		return line[:-1]
	else:
		return line

class DiffModel:
	"""An abstract model of the differences between 2 files."""

	class DiffLine:
		"""Abstract representation of a line in a diff."""

		def __init__( self, left, right, status ):
			"""Create a DiffLine.
			- left is the line in the left file, or
			  None if this is an ADD line.
			- right is the line in the right file, or
			  None if this is a REMOVE line.
			- status is a constant from lib.difflinetypes describing the type
			  of line this is: IDENTICAL, DIFFERENT, ADD or REMOVE."""

			self.left = left
			self.right = right
			self.status = status

		def __repr__( self ):
			return "%s -- %s" % ( self.left, self.right )

	def __init__( self, parser ):
		self.parser = parser
		self.lines = []

	def get_lines( self ):
		self.parser.parse_lines( self.line_callback )
		return self.lines

	def get_num_lines( self ):
		return len( self.lines )

	def line_callback( self, left, right, status ):
		"""Receive a callback from the parser saying that we have received a
		line."""
		self.lines.append( DiffModel.DiffLine( strip_newline( left ),
			strip_newline( right ), status ) )

