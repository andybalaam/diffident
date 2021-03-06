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

class cursor_column_state( object ):
	COLUMN_ALL    = 0
	COLUMN_SINGLE = 1

class difflinetypes( object ):
	"""The types of diff line there can be."""
	DIFFERENT    = 0
	IDENTICAL    = 1
	ADD          = 2
	REMOVE       = 3

class directions( object ):
	LEFT  = 0
	RIGHT = 1
	UP    = 2
	DOWN  = 3

	def opposite_lr( side ):
		if side == directions.LEFT:
			return directions.RIGHT
		elif side == directions.RIGHT:
			return directions.LEFT
		else:
			raise Exception( "Expected either LEFT or RIGHT.  Got '%s'."
				% str( side ) )
	opposite_lr = staticmethod(opposite_lr) 

class save_status( object ):
	STATUS_SAVED     = 0
	STATUS_NOCHANGES = 1

class keys( object ):
	KEY_ESCAPE = 27


