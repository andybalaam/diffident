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

from test.asserts import assert_strings_equal

from lib.diffline import DiffLine
from testlib.fakediffmodel import FakeDiffModel

from lib.constants import save_status
from lib.constants import difflinetypes

from lib.ncursesview import NCursesView

def default_message_at_start():

	diffmodel = FakeDiffModel()
	diffmodel.lines = []

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 5

	actions = []

	assert_strings_equal( view.show( actions )[2],
"""[ni]         Press SHIFT-H for help         
""" )

class AlwaysSaveFileManager:
	def save( self, diffmodel, lr ):
		return save_status.STATUS_SAVED

def file_saved():

	diffmodel = FakeDiffModel()
	diffmodel.lines = []

	filemanager = AlwaysSaveFileManager()
	view = NCursesView( diffmodel, None, None, filemanager )
	view.win_width  = 40
	view.win_height = 5

	actions = [ "s" ]

	assert_strings_equal( view.show( actions )[2],
"""[mi]              File saved.               
""" )

class NeverSaveFileManager:
	def save( self, diffmodel, lr ):
		return save_status.STATUS_NOCHANGES

def no_need_to_save():

	diffmodel = FakeDiffModel()
	diffmodel.lines = []

	filemanager = NeverSaveFileManager()
	view = NCursesView( diffmodel, None, None, filemanager )
	view.win_width  = 40
	view.win_height = 5

	actions = [ "s" ]

	assert_strings_equal( view.show( actions )[2],
"""[mi]   No changes were made in this file.   
""" )

def default_message_after_move():

	diffmodel = FakeDiffModel()
	diffmodel.lines = []

	filemanager = AlwaysSaveFileManager()
	view = NCursesView( diffmodel, None, None, filemanager )
	view.win_width  = 40
	view.win_height = 5

	actions = [ "s", "j" ]

	assert_strings_equal( view.show( actions )[2],
"""[ni]         Press SHIFT-H for help         
""" )

def help():

	diffmodel = FakeDiffModel()
	diffmodel.lines = []

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 40

	actions = [ "H" ]

	assert_strings_equal( view.show( actions )[2],
"""[ni]       Press any key to continue        
""" )


def after_last_difference():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( "line 01", "line 01", difflinetypes.IDENTICAL ),
		DiffLine( "line 02", "line 02", difflinetypes.DIFFERENT ),
		DiffLine( "line 03", "line 03", difflinetypes.IDENTICAL ),
	]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 5

	actions = [ "n", "j", "n" ]

	assert_strings_equal( view.show( actions )[2],
"""[mi]         After last difference          
""" )

def at_last_difference():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( "line 01", "line 01", difflinetypes.IDENTICAL ),
		DiffLine( "line 02", "line 02", difflinetypes.DIFFERENT ),
		DiffLine( "line 03", "line 03", difflinetypes.IDENTICAL ),
	]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 5

	actions = [ "n", "n" ]

	assert_strings_equal( view.show( actions )[2],
"""[mi]           At last difference           
""" )


def before_first_difference():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( "line 01", "line 01", difflinetypes.IDENTICAL ),
		DiffLine( "line 02", "line 02", difflinetypes.DIFFERENT ),
		DiffLine( "line 03", "line 03", difflinetypes.IDENTICAL ),
	]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 5

	actions = [ "p" ]

	assert_strings_equal( view.show( actions )[2],
"""[mi]        Before first difference         
""" )


def at_first_difference():

	diffmodel = FakeDiffModel()
	diffmodel.lines = [
		DiffLine( "line 01", "line 01", difflinetypes.IDENTICAL ),
		DiffLine( "line 02", "line 02", difflinetypes.DIFFERENT ),
		DiffLine( "line 03", "line 03", difflinetypes.IDENTICAL ),
	]

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 5

	actions = [ "n", "p" ]

	assert_strings_equal( view.show( actions )[2],
"""[mi]          At first difference           
""" )



def run():
	default_message_at_start()
	file_saved()
	no_need_to_save()
	default_message_after_move()
	help()
	after_last_difference()
	at_last_difference()
	before_first_difference()
	at_first_difference()

