#!/usr/bin/python

import sys

from test.test_all import test_all

def main():
	if len( sys.argv ) > 1 and sys.argv[1] == "--test":
		return test_all()

	print "Usage: ./diffident.py --test"
	sys.exit( 1 )

if __name__ == "__main__":
	main()


