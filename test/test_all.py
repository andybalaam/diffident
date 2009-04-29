import os

import test_listview
import test_diffmodel
import test_ncursesview
import test_ncursesview_movement
import test_ncursesview_nextdiff
import test_unifieddiffparser

def run_quick_tests():
	test_listview.run()
	test_diffmodel.run()
	test_unifieddiffparser.run()

def run_medium_tests():
	test_ncursesview.run()
	test_ncursesview_movement.run()
	test_ncursesview_nextdiff.run()

def test_quick():
	run_quick_tests()
	print "All tests passed."
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

