
class FakeDiffModel:
	def __init__( self ):
		self.lines = []

	def get_lines( self ):
		return self.lines

	def get_num_lines( self ):
		return len( self.lines )

