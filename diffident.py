#!/usr/bin/python

import sys

import lib.main
import test.test_all

def main():
	if len( sys.argv ) > 1:
		if sys.argv[1] == "--test":
			return test.test_all.test_quick()
		elif sys.argv[1] == "--test-slow":
			return test.test_all.test_slow()

	if len( sys.argv ) > 2:
		return lib.main.emulate_diff_minus_y( sys.argv[1], sys.argv[2] )

	sys.stderr.write( """Usage:
./diffident.py file1 file2
./diffident.py --test
./diffident.py --test-slow
""" )
	sys.exit( 1 )

if __name__ == "__main__":
	main()


