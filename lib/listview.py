
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
			pattern = "%%-%ds <> %%-%ds\n" % ( half_width, half_width )
			ret += pattern % ( line.left, line.right )
		return ret

