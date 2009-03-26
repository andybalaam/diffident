
def is_x_line( line, x ):
	return ( line[0] == x and not line.startswith( x * 3 ) )

def is_minus_line( line ):
	return is_x_line( line, "-" )

def is_plus_line( line ):
	return is_x_line( line, "+" )

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
		ret = []
		left_lines = []

		for line in self.diff:
			if is_minus_line( line ):
				left_lines.append( line[1:] )
			elif is_plus_line( line ):
				ret.append( DiffModel.DiffLine( left_lines[0], line[1:] ) )
				left_lines = left_lines[1:]

		return ret


