
class DiffModel:
	"""An abstract model of the differences between 2 files."""

	class DiffLine:
		def __init__( self, left, right, status ):
			self.left = left
			self.right = right
			self.status = status

		def __repr__( self ):
			return "%s -- %s" % ( self.left, self.right )

	def __init__( self, parser ):
		self.parser = parser

	def get_lines( self ):
		return self.parser.parse_lines()


