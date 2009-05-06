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

from testlib.fakediffline import FakeDiffLine
from testlib.fakediffmodel import FakeDiffModel

import lib.difflinetypes as difflinetypes
from lib.ncursesview import NCursesView

def header_short_names():

	diffmodel = FakeDiffModel()
	diffmodel.lines = []

	view = NCursesView( diffmodel,
		"dir1/file1.txt", "dir2/file2.txt" )
	view.win_width  = 40
	view.win_height = 5

	actions = []

	assert_strings_equal( view.show( actions )[1],
"""[ni]dir1/file1.txt       dir2/file2.txt     
""" )

def header_long_names():

	diffmodel = FakeDiffModel()
	diffmodel.lines = []

	view = NCursesView( diffmodel,
		"dir1/dir2/dir3/dir4/dir5/file1.txt", "dira/dirb/dirc/dird/dire/file2.txt" )
	view.win_width  = 40
	view.win_height = 5

	actions = []

	assert_strings_equal( view.show( actions )[1],
"""[ni].../dir5/file1.txt   ...d/dire/file2.txt
""" )

def status_default():

	diffmodel = FakeDiffModel()
	diffmodel.lines = []

	view = NCursesView( diffmodel )
	view.win_width  = 40
	view.win_height = 5

	actions = []

	assert_strings_equal( view.show( actions )[2],
"""[ni]         Press SHIFT-H for help         
""" )


def run():
	header_short_names()
	header_long_names()
	status_default()
