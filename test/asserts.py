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

def assert_strings_equal( str1, str2 ):
	if str1 == str2:
		return

	str1 = str1.replace( " ", "." )
	str2 = str2.replace( " ", "." )

	print str1 + "\n!= \n" + str2

	char = None
	for i in xrange( min( len( str1 ),
			len( str2 ) ) ):
		if str1[i] != str2[i]:
			char = i
			break

	if char is None:
		if len( str1 ) > len( str2 ):
			print "The first one is longer."
		else:
			print "The second one is longer."
	else:
		print "At character %d, %s != %s" % (
			char, str1[char], str2[char] )

	raise AssertionError()

