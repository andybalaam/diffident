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

from lib.parsers.unifieddiffparser import UnifiedDiffParser
from lib.diffmodels.diffmodel import DiffModel
from lib.diffmodels.editablediffmodel import EditableDiffModel
from lib.misc.filemanager import FileManager
from lib.views.listview import ListView
from lib.views.ncursesview import NCursesView

def diff_2_files( filename_left, filename_right, launch_viewer, sendkeys ):

	# TODO: do this properly - handle errors, suck stderr from diff,
	#       don't use os.system, and use a proper temporary file path.
	#       Generally don't be so lazy, and buck your ideas up.

	diff_filename = "tmpdiff.tmpdiffident"
	os.system( 'diff -u "%s" "%s" > %s' % (
		filename_left, filename_right, diff_filename ) )

	diff_file = file( diff_filename, 'r' )
	left_file = file( filename_left, 'r' )

	diffparser = UnifiedDiffParser( left_file, diff_file )
	diffmodel = DiffModel( diffparser )
	editablediffmodel = EditableDiffModel( diffmodel )
	filemanager = FileManager( filename_left, filename_right )

	launch_viewer( editablediffmodel, filename_left, filename_right,
		filemanager, sendkeys )

	left_file.close()
	diff_file.close()

	os.remove( diff_filename )

def print_listview( diffmodel, filename_left, filename_right, filemanager,
		sendkeys ):
	listview = ListView( diffmodel )
	print listview.get_string(),

def run_ncursesview( diffmodel, filename_left, filename_right, filemanager,
		sendkeys ):
	ncursesview = NCursesView( diffmodel, filename_left, filename_right,
		filemanager )
	ncursesview.show( sendkeys )

def emulate_diff_minus_y( filename_left, filename_right ):
	diff_2_files( filename_left, filename_right, print_listview, None )

def interactive_diff_ncurses( filename_left, filename_right, sendkeys ):
	diff_2_files( filename_left, filename_right, run_ncursesview, sendkeys )



