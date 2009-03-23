
class ListView:
	def __init__( self, diffmodel ):
		self.diffmodel = diffmodel
		self.columns = 80

	def set_columns( self, columns ):
		self.columns = columns

	def get_string( self ):
		ret = ""
		lines = self.diffmodel.get_lines()
		for line in lines:
			ret += "%-37s <> %-37s\n" % ( line.left, line.right )
		return ret

