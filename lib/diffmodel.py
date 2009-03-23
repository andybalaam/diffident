
class DiffModel:

	class DiffLine:
		def __init__( self, left, right ):
			self.left = left
			self.right = right

	def __init__( self, left_file, right_file, diff ):
		self.left_file = left_file
		self.right_file = right_file
		self.diff = diff

	def get_lines( self ):
		return [
			DiffModel.DiffLine( "line 1 here", "line 1 here different" ),
			DiffModel.DiffLine( "line 2 here", "line 2 here different" ),
		]


