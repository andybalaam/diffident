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

import itertools

def reversed_enumerate( sequence ):
	"""Provide an iterator that generates the items in the supplied
	sequence in reverse order, paired with the index number of each
	item in the list.

	Example:
	>>> list( reversed_enumerate( ["a", "b", "c"] ) )
	[(2, 'c'), (1, 'b'), (0, 'a')]

	Credit goes to Christophe Simonis for the idea of using izip to do this:
	http://christophe-simonis-at-tiny.blogspot.com/2008/08/python-reverse-enumerate.html
	"""

	backwards_counter = xrange( len( sequence ) - 1, -1, -1 )

	return itertools.izip( backwards_counter, reversed( sequence ) )


