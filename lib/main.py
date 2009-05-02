#   Diffident, an interactive diff viewer and editor
#   Copyright (C) 2009 Andy Balaam <axis3x3@users.sf.net>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

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



