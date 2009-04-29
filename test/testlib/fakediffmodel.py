
class FakeDiffModel:
	def __init__( self ):
		self.lines = []

	def get_lines( self, start=0, end=None ):
		if end is None:
			return self.lines[start:]
		else:
			return self.lines[start:end]

	def get_num_lines( self ):
		return len( self.lines )

