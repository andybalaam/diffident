import os

from lib.unifieddiffparser import UnifiedDiffParser
from lib.diffmodel import DiffModel
from lib.listview import ListView
from lib.ncursesview import NCursesView

def diff_2_files( filename1, filename2, launch_viewer ):

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

	launch_viewer( diffmodel )

	left_file.close()
	diff_file.close()

	os.remove( diff_filename )

def print_listview( diffmodel ):
	listview = ListView( diffmodel )
	print listview.get_string(),

def run_ncursesview( diffmodel ):
	ncursesview = NCursesView( diffmodel )
	ncursesview.show()

def emulate_diff_minus_y( filename1, filename2 ):
	diff_2_files( filename1, filename2, print_listview )

def interactive_diff_ncurses( filename1, filename2 ):
	diff_2_files( filename1, filename2, run_ncursesview )



