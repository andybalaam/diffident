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

import test_diffidenttools
import test_diffmodel
import test_editablediffmodel
import test_listview
import test_ncursesview
import test_ncursesview_editing
import test_ncursesview_header
import test_ncursesview_helpscreen
import test_ncursesview_multiselect
import test_ncursesview_movement
import test_ncursesview_nextdiff
import test_ncursesview_status
import test_unifieddiffparser

def run_quick_tests():
	test_diffidenttools.run()
	test_diffmodel.run()
	test_editablediffmodel.run()
	test_listview.run()
	test_unifieddiffparser.run()

def run_medium_tests():
	test_ncursesview.run()
	test_ncursesview_editing.run()
	test_ncursesview_header.run()
	test_ncursesview_helpscreen.run()
	test_ncursesview_movement.run()
	test_ncursesview_multiselect.run()
	test_ncursesview_nextdiff.run()
	test_ncursesview_status.run()

def test_quick():
	run_quick_tests()
	print "All quick tests passed."
	return 0

def test_medium():
	run_quick_tests()
	run_medium_tests()
	print "All tests passed."
	return 0

def test_slow():
	run_quick_tests()
	run_medium_tests()

	# TODO: don't use os.system, and handle return values correctly.
	retval = os.system( "test/slow/test_slow.sh" )
	if retval == 0:
		print "All tests (including slow ones) passed."

	return retval

