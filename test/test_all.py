import os

import test_listview
import test_diffmodel
import test_unifieddiffparser

def run_quick_tests():
	test_listview.run()
	test_diffmodel.run()
	test_unifieddiffparser.run()

def test_quick():
	run_quick_tests()
	print "All tests passed."
	return 0

def test_slow():
	run_quick_tests()

	# TODO: don't use os.system, and handle return values correctly.
	retval = os.system( "test/slow/test_slow.sh" )
	if retval == 0:
		print "All tests (including slow ones) passed."

