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

import difflinetypes

NEXT_DIFF_MARGIN = 3

class NCursesView( object ):

	LEFT  = 0
	RIGHT = 1
	UP    = 2
	DOWN  = 3

	class Cursor( object ):
		def __init__( self, lr, line_num ):
			self.lr = lr
			self.line_num = line_num

	def __init__( self, diffmodel ):
		self.diffmodel = diffmodel
		self.top_line = None
		self.bot_line = None
		self.first_col = 0
		self.mycursor = NCursesView.Cursor( NCursesView.LEFT, 0 )
		self.win_height = None # Modify these in test code
		self.win_width = None  #

	def show( self, debug_actions=None ):
		return curses.wrapper( self.show_impl, debug_actions )

	def show_impl( self, stdscr, debug_actions ):
		self.stdscr = stdscr

		curses.curs_set( 0 )

		self.make_color_pairs()

		# If we are in test code and have modified these, leave them.
		# Otherwise, get them from the environment
		if self.win_height is None:
			( self.win_height, self.win_width ) = self.stdscr.getmaxyx()
			self.win_width -= 1

		win_width_without_mid_col = self.win_width - 3
		self.left_width  = win_width_without_mid_col // 2
		self.right_width = win_width_without_mid_col - self.left_width
		self.mid_col     = self.left_width
		self.right_start = self.left_width + 3

		self.set_top_line( 0 )

		self.stdscr.bkgd( ord( " " ), self.CP_NORMAL )

		self.draw_screen()

		#self.main_loop()

		# If debug_actions is None we wait for user input
		if debug_actions is None:
			self.main_loop()
		else:
			# Otherwise we have a list of things to do and then
			# take a screenshot and return it
			for action in debug_actions:
				if isinstance( action, str ):
					action = ord( action )
				self.process_keypress( action )
			return self.take_screenshot()

	def set_top_line( self, top_line ):
		self.top_line = top_line
		self.bot_line = self.top_line + self.win_height
		self.lines = self.diffmodel.get_lines( self.top_line, self.bot_line )

	def main_loop( self ):

		keep_going = True
		while keep_going:
			key = self.stdscr.getch()
			keep_going = self.process_keypress( key )

	def process_keypress( self, key ):
		keep_going = True
		if key == ord( "q" ): # Quit
			keep_going = False
		elif key == ord( "h" ) or key == curses.KEY_LEFT:
			self.move_cursor( NCursesView.LEFT )
		elif key == ord( "l" ) or key == curses.KEY_RIGHT:
			self.move_cursor( NCursesView.RIGHT )
		elif key == ord( "j" ) or key == curses.KEY_DOWN:
			self.move_cursor( NCursesView.DOWN )
		elif key == ord( "k" ) or key == curses.KEY_UP:
			self.move_cursor( NCursesView.UP )
		elif key == ord( "." ) or key == curses.KEY_NPAGE: # Page down
			self.change_page( 1 )
		elif key == ord( "," ) or key == curses.KEY_PPAGE: # Page up
			self.change_page( -1 )
		elif key == ord( "n" ) or key == curses.KEY_F8: # Next difference
			self.next_difference( 1 )
		elif key == ord( "p" ) or key == curses.KEY_F7: # Previous difference
			self.next_difference( -1 )
		elif key == ord( "z" ): # Scroll left
			self.scroll_horizontal( -1 )
		elif key == ord( "x" ): # Scroll right
			self.scroll_horizontal( 1 )
		return keep_going

	def get_horizontal_scroll_width( self ):
		return ( self.left_width // 2 )

	def scroll_horizontal( self, dr ):
		old_first_col = self.first_col
		scroll_width = self.get_horizontal_scroll_width()
		self.first_col += ( dr * scroll_width )
		if self.first_col < 0:
			self.first_col = 0
		elif self.scrolled_off_right():
			self.first_col = old_first_col

		if old_first_col != self.first_col:
			self.draw_screen()

	def line_visible_horizontally( self, linestr ):
		"""Return True if this line is long enough to show up
		at the current horizontal scroll position."""
		return ( linestr is not None and
			len( linestr ) > self.first_col )

	def scrolled_off_right( self ):
		"""Returns true if we have scrolled so far right
		that there is nothing on the screen."""

		# If we're not scrolled right at all, this question
		# is irrelevant
		if self.first_col == 0:
			return False

		# If any line is long enough, we are not scrolled
		# too far.
		for line in self.lines:
			if ( self.line_visible_horizontally( line.left ) or
			     self.line_visible_horizontally( line.right ) ):
				return False

		# None of the lines were long enough, so we are
		# scrolled too far.
		return True

	def move_cursor( self, dr ):
		# TODO: don't redraw whole screen when scrolling?

		redraw = False

		if dr == NCursesView.LEFT and self.mycursor.lr == NCursesView.RIGHT:
			self.mycursor.lr = NCursesView.LEFT
			self.refresh_cursor_line()
		elif dr == NCursesView.RIGHT and self.mycursor.lr == NCursesView.LEFT:
			self.mycursor.lr = NCursesView.RIGHT
			self.refresh_cursor_line()
		elif dr == NCursesView.UP:
			if self.mycursor.line_num == 0:
				if self.top_line > 0:
					self.set_top_line( self.top_line - 1 )
					redraw = True
			else:
				self.add_to_cursor_and_refresh( -1 )
		elif dr == NCursesView.DOWN:
			if self.mycursor.line_num == ( self.win_height - 1 ):
				if self.bot_line < self.diffmodel.get_num_lines():
					self.set_top_line( self.top_line + 1 )
					redraw = True
			else:
				self.add_to_cursor_and_refresh( 1 )
		if redraw:
			self.draw_screen()

	def add_to_cursor_and_refresh( self, direction ):
		old_line_num = self.mycursor.line_num
		self.mycursor.line_num += direction
		self.draw_single_line( old_line_num )
		self.draw_single_line( self.mycursor.line_num )
		self.stdscr.refresh()

	def refresh_cursor_line( self ):
		self.draw_single_line( self.mycursor.line_num )
		self.stdscr.refresh()

	def change_page( self, direction ):
		top_line = self.top_line
		top_line += direction * self.win_height
		if top_line < 0:
			top_line = 0
		elif top_line > self.diffmodel.get_num_lines() - self.win_height:
			top_line = self.diffmodel.get_num_lines() - self.win_height

		redraw = False
		if top_line != self.top_line:
			# Normal case - move down a page and don't move the cursor
			self.set_top_line( top_line )
			redraw = True
		elif top_line == 0 and self.mycursor.line_num != 0:
			# We hit the top - move the cursor up to the top
			self.mycursor.line_num = 0
			redraw = True
		elif ( self.bot_line == self.diffmodel.get_num_lines() and
				self.mycursor.line_num != self.win_height - 1 ):
			# We hit the bottom - move the cursor down to the bottom
			self.mycursor.line_num = self.win_height - 1
			redraw = True

		if redraw:
			while self.scrolled_off_right():
				self.first_col -= self.get_horizontal_scroll_width()
				if self.first_col < 0:
					self.first_col = 0

			self.draw_screen()

	def next_difference( self, direction ):
		current_pos = self.top_line + self.mycursor.line_num

		# Skip the difference we are in
		line = self.diffmodel.get_line( current_pos )
		while ( line is not None and
				line.status != difflinetypes.IDENTICAL ):
			current_pos += direction
			line = self.diffmodel.get_line( current_pos )

		# Find the next difference
		while ( line is not None and
				line.status == difflinetypes.IDENTICAL ):
			current_pos += direction
			line = self.diffmodel.get_line( current_pos )

		# Go to the beginning of the found difference
		if line is not None and direction == -1:
			prev_line = line
			while( prev_line is not None and
					prev_line.status != difflinetypes.IDENTICAL ):
				line = prev_line
				current_pos += direction
				prev_line = self.diffmodel.get_line( current_pos )
			# current_pos overshot by 1 - correct it
			current_pos -= direction

		if line is not None:
			top_line = current_pos - NEXT_DIFF_MARGIN
			curs_pos = NEXT_DIFF_MARGIN
			if top_line < 0:
				curs_pos += top_line
				top_line = 0
			self.set_top_line( top_line )
			self.mycursor.line_num = curs_pos

			self.draw_screen()
		else:
			pass # TODO: status line message

	def make_color_pairs( self ):
		curses.use_default_colors()

		self.CP_NORMAL = self.create_color_pair(
			1, -1, -1)
		self.CP_DIFFERENT  = self.create_color_pair(
			2, curses.COLOR_BLUE,  -1 )
		self.CP_ADD = self.create_color_pair(
			3, curses.COLOR_GREEN, -1 )
		self.CP_REMOVE = self.create_color_pair(
			4, curses.COLOR_RED, -1 )
		self.CP_MISSING = self.create_color_pair(
			5, curses.COLOR_YELLOW, -1 )

	def create_color_pair( self, pair_num, fore, back ):
		curses.init_pair( pair_num, fore, back )
		return curses.color_pair( pair_num )

	def draw_screen( self ):
		self.stdscr.clear()

		for line_num, ln in enumerate( self.lines ):
			self.write_line( ln, line_num )

		self.stdscr.refresh()

	def draw_single_line( self, line_num ):
		ln = self.lines[line_num]
		self.write_line( ln, line_num )

	def write_line( self, ln, line_num ):

		if ln.status == difflinetypes.IDENTICAL:
			left_colour_pair  = self.CP_NORMAL
			right_colour_pair = self.CP_NORMAL
			mid_colour_pair = self.CP_NORMAL
			mid_char = " "
		elif ln.status == difflinetypes.DIFFERENT:
			left_colour_pair  = self.CP_DIFFERENT
			right_colour_pair = self.CP_DIFFERENT
			mid_colour_pair = self.CP_DIFFERENT | curses.A_REVERSE
			mid_char = "*"
		elif ln.status == difflinetypes.ADD:
			left_colour_pair  = self.CP_MISSING
			right_colour_pair = self.CP_ADD
			mid_colour_pair = self.CP_ADD | curses.A_REVERSE
			mid_char = "+"
		elif ln.status == difflinetypes.REMOVE:
			left_colour_pair  = self.CP_REMOVE
			right_colour_pair = self.CP_MISSING
			mid_colour_pair = self.CP_REMOVE | curses.A_REVERSE
			mid_char = "-"
		else:
			raise Exception( "Unknown line type %d." % ln.status )

		if self.mycursor.line_num == line_num:
			if self.mycursor.lr == NCursesView.LEFT:
				left_colour_pair  |= curses.A_REVERSE
			else:
				right_colour_pair |= curses.A_REVERSE

		left  = self.pad_to_width( ln.left, self.first_col, self.left_width )
		right = self.pad_to_width( ln.right, self.first_col, self.right_width )

		self.stdscr.addnstr( line_num, 0, left, self.left_width,
			left_colour_pair )
		self.stdscr.addnstr( line_num, self.right_start, right,
			self.right_width, right_colour_pair )
		self.stdscr.addnstr( line_num, self.mid_col,
			" %s " % mid_char, 3, mid_colour_pair )

	def pad_to_width( self, string, first_col, width ):
		if string is None:
			return "." * width
		string = string.expandtabs()[first_col:]
		return string + ( " " * ( width - len( string ) ) )

	# Testing code

	def attr_to_string( self, attr ):
		if attr == 1:
			attr_str = "n" # Normal
		elif attr == 2:
			attr_str = "d" # Different
		elif attr == 3:
			attr_str = "a" # Add
		elif attr == 4:
			attr_str = "r" # Remove
		elif attr == 5:
			attr_str = "m" # Missing
		elif attr == 1025:
			attr_str = "ni" # Normal-Inverse
		elif attr == 1026:
			attr_str = "di" # etc...
		elif attr == 1027:
			attr_str = "ai"
		elif attr == 1028:
			attr_str = "ri"
		elif attr == 1029:
			attr_str = "mi"
		else:
			attr_str = str( attr )

		return "[%s]" % attr_str

	def take_screenshot( self ):
		ret = ""
		prev_attr = -1
		for y in xrange( self.win_height ):
			for x in xrange( self.win_width ):
				ch_plus_attrs = self.stdscr.inch( y, x )
				ch = chr( ch_plus_attrs & 0xFF )
				attr = ch_plus_attrs >> 8
				if attr != prev_attr:
					prev_attr = attr
					ret += self.attr_to_string( attr )
				ret += ch
			ret += "\n"
		return ret


