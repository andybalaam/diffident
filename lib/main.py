import os

from lib.unifieddiffparser import UnifiedDiffParser
from lib.diffmodel import DiffModel
from lib.listview import ListView

def diff_2_files( filename1, filename2 ):

	# TODO: do this properly - handle errors, suck stderr from diff,
	#       don't use os.system, and use a proper temporary file path.
	#       Generally don't be so lazy, and buck your ideas up.

	diff_filename = "tmpdiff.tmpdiffident"
	os.system( 'diff -u "%s" "%s" > %s' % (
		filename1, filename2, diff_filename ) )

	diff_file = file( diff_filename, 'r' )
	left_file = file( filename1, 'r' )

	diffparser = UnifiedDiffParser( left_file, diff_file )
	diffmodel = DiffModel( diffparser )

	listview = ListView( diffmodel )

	print listview.get_string(),

	left_file.close()
	diff_file.close()

	os.remove( diff_filename )


