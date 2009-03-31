import lib.difflinetypes as difflinetypes

def empty_if_none( line ):
	if line is None:
		return ""
	else:
		return line

class ListView:
	"""A simple view on a DiffModel that just lists all the lines in a file
	side by side."""

	def __init__( self, diffmodel ):
		self.diffmodel = diffmodel
		self.columns = 80

	def set_columns( self, columns ):
		self.columns = columns

	def get_string( self ):

		half_width = int( ( self.columns - 4 ) / 2 )

		ret = ""
		lines = self.diffmodel.get_lines()
		for line in lines:
			if line.status == difflinetypes.IDENTICAL:
				divider = "   "
			elif line.status == difflinetypes.DIFFERENT:
				divider = "|  "
			elif line.status == difflinetypes.ADD:
				divider = ">  "
			elif line.status == difflinetypes.REMOVE:
				divider = "<"
			else:
				raise Exception( "Unknown line type %d." % line.status )

			pattern = "%%-%ds %s%%s\n" % ( half_width, divider )
			ret += pattern % ( empty_if_none( line.left ),
				empty_if_none( line.right ) )
		return ret

