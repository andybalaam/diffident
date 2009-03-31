#!/usr/bin/python

import sys

from test.test_all import test_quick
from test.test_all import test_slow

from lib.main import diff_2_files

def main():
	if len( sys.argv ) > 1:
		if sys.argv[1] == "--test":
			return test_quick()
		elif sys.argv[1] == "--test-slow":
			return test_slow()

	if len( sys.argv ) > 2:
		return diff_2_files( sys.argv[1], sys.argv[2] )

	sys.stderr.write( """Usage:
./diffident.py file1 file2
./diffident.py --test
./diffident.py --test-slow
""" )
	sys.exit( 1 )

if __name__ == "__main__":
	main()


