
class FakeDiffModel:
	def __init__( self ):
		self.lines = []

	def get_lines( self, start=0, end=None ):
		if end is None:
			return self.lines[start:]
		else:
			return self.lines[start:end]

	def get_line( self, line_num ):
		if 0 <= line_num < len( self.lines ):
			return self.lines[line_num]
		else:
			return None

	def get_num_lines( self ):
		return len( self.lines )

