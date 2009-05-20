#!/usr/bin/python

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

import optparse
import sys

import lib.main
import test.test_all

def main():

	parser = optparse.OptionParser( usage="%prog [options] file1 file2",
		version="diffident-0.1" )

	parser.add_option("", "--view", dest="view",
		default="term", type="string",
		help=( "Set the view type: "
			+ "list (somewhat emulates diff -y), "
			+ "or term (interactive editable diff in a terminal)"
			# (not yet!) "or gtk (interactive editable diff in a GTK IU)."
			) )

	parser.add_option("", "--send-keys", dest="sendkeys",
		default=None, type="string",
		help="'Press' these keys after starting, then exit "
			+ "(used for testing)." )

	parser.add_option("", "--test", dest="test",
		default=False, action="store_true",
		help="Run the ncurses and super-fast unit tests." )

	parser.add_option("", "--test-quick", dest="test_quick",
		default=False, action="store_true",
		help="Run only super-fast unit tests." )

	parser.add_option("", "--test-slow", dest="test_slow",
		default=False, action="store_true",
		help="Run the slow, medium and quick unit tests."
			+ "  The slow tests involve e.g. disk access and shell commands.")

	( options, args ) = parser.parse_args()

	if options.test_slow:
		return test.test_all.test_slow()
	elif options.test_quick:
		return test.test_all.test_quick()
	elif options.test:
		return test.test_all.test_medium()

	if len( args ) != 2:
		parser.error( "You must supply 2 files to compare." )

	if options.view == "list":
		return lib.main.emulate_diff_minus_y( args[0], args[1] )
	elif options.view == "term":
		return lib.main.interactive_diff_ncurses( args[0], args[1],
			options.sendkeys )
	elif options.view == "gtk":
		sys.stderr.write( "GTK UI not yet supported!\n" )
		sys.exit( 1 )
	else:
		sys.stderr.write( "Unknown view '%s'.\n" % options.view )
		sys.exit( 2 )

if __name__ == "__main__":
	main()


