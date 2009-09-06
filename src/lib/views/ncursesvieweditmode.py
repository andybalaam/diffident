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

import curses

from lib.misc.constants import cursor_column_state
from lib.misc.constants import keys

from lib.misc.translation import _

class NCursesViewEditMode( object ):
	def __init__( self, parent_ncursesview ):
		self.v = parent_ncursesview

	def run( self, debug_actions ):

		self.v.set_status_line( _("Editing line.  Press ESC to finish."), True )
		self.v.mycursor.column_status = cursor_column_state.COLUMN_SINGLE
		self.v.refresh_cursor_line()

		if debug_actions is None:
			self.main_loop()
		else:
			for action in debug_actions:
				if isinstance( action, str ):
					action = ord( action )
				keep_going = self.process_keypress( action )
				if not keep_going:
					break
			else:
				return -1

		self.v.mycursor.column_status = cursor_column_state.COLUMN_ALL
		self.v.refresh_cursor_line()
		self.v.set_status_line( self.v.DEFAULT_STATUS_MESSAGE, False )

	def main_loop( self ):
		keep_going = True
		while keep_going:
			key = self.v.stdscr.getch()
			keep_going = self.process_keypress( key )

	def process_keypress( self, key ):
		keep_going = True

		if key == keys.KEY_ESCAPE: # Stop editing
			keep_going = False

		return keep_going

