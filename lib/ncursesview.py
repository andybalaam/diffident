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

from translation import _

NEXT_DIFF_MARGIN = 3

DEFAULT_STATUS_MESSAGE = _("Press SHIFT-H for help")

HELP_MESSAGES = [
	"",
	_("Diffident Help"),
	"",
	( _("Quit"), _("q") ),
	( _("Move"), _("hjkl or Arrow Keys") ),
	( _("Next/Previous"), _("n/p or F8/F7") ),
	( _("Page Up/Down"), _(",/. or PageUp/Down") ),
	( _("Scroll Left/Right"), _("z/x") ),
]

COPYRIGHT_MESSAGES = [
	"Diffident is Copyright (C) 2009 Andy Balaam and the Diffident developers.",
	"Diffident comes with ABSOLUTELY NO WARRANTY.",
	"This is free software, and you are welcome to redistribute it under certain",
	"conditions; see the file COPYING for details, or gnu.org/licenses/gpl-2.0.txt",
]

class NCursesView( object ):

	LEFT  = 0
	RIGHT = 1
	UP    = 2
	DOWN  = 3

	class Cursor( object ):
		def __init__( self, lr, line_num ):
			self.lr = lr
			self.set_line_num( line_num, False )

		def add_to_line_num( self, inc, shift_pressed ):
			self.set_line_num( self.line_num + inc, shift_pressed )

		def set_line_num( self, new_value, shift_pressed ):
			self.line_num = new_value
			if not shift_pressed:
				self.start_line_num = new_value

		def shift_selection( self, inc ):
			self.start_line_num += inc

		def is_line_selected( self, line_num ):
			return ( self.start_line_num <= line_num <= self.line_num or
			         self.start_line_num >= line_num >= self.line_num )

		def get_selected_range( self ):
			"""Return a range generator that covers all selected lines."""

			if self.start_line_num <= self.line_num:
				return xrange( self.start_line_num, self.line_num + 1 )
			else:
				return xrange( self.line_num, self.start_line_num + 1 )

	def __init__( self, diffmodel, filename1 = None, filename2 = None ):
		self.diffmodel = diffmodel
		self.filename1 = filename1
		self.filename2 = filename2
		self.top_line = 0
		self.bot_line = None
		self.first_col = 0
		self.mycursor = NCursesView.Cursor( NCursesView.LEFT, 0 )
		self.win_height = None # Modify these in test code
		self.win_width = None  #

	def show( self, debug_actions=None ):
		return curses.wrapper( self.show_impl, debug_actions )

	def show_impl( self, stdscr, debug_actions ):
		self.stdscr = stdscr
		self.stdscr.refresh()
		# If we are in test code and have modified these, leave them.
		# Otherwise, get them from the environment
		if self.win_height is None:
			( self.win_height, self.win_width ) = stdscr.getmaxyx()
			self.win_height -= 2
			self.win_width -= 1

		self.textwindow = curses.newwin(
			self.win_height, self.win_width + 1, 1, 0 )

		self.headerwindow = curses.newwin( 1, self.win_width + 1, 0, 0 )

		self.statuswindow = curses.newwin(
			1, self.win_width + 1, self.win_height + 1, 0 )

		curses.curs_set( 0 )

		self.make_color_pairs()

		win_width_without_mid_col = self.win_width - 3
		self.left_width  = win_width_without_mid_col // 2
		self.right_width = win_width_without_mid_col - self.left_width
		self.mid_col     = self.left_width
		self.right_start = self.left_width + 3

		self.textwindow.bkgd( ord( " " ), self.CP_NORMAL )
		self.headerwindow.bkgd( ord( " " ),
			self.CP_NORMAL | curses.A_REVERSE )
		self.statuswindow.bkgd( ord( " " ),
			self.CP_NORMAL | curses.A_REVERSE )

		self.draw_header_window()
		self.set_status_line( DEFAULT_STATUS_MESSAGE, False )

		self.set_top_line( 0 )
		self.draw_screen()

		# If debug_actions is None we wait for user input
		if debug_actions is None:
			self.main_loop()
		else:
			# Otherwise we have a list of things to do and then
			# take a screenshot and return it
			for action in debug_actions:
				if isinstance( action, str ):
					action = ord( action )
				self.process_keypress( action, False )
			return ( self.screenshot_textwindow(),
				self.screenshot_header(),
				self.screenshot_status() )

	def set_top_line( self, top_line ):
		self.mycursor.shift_selection( self.top_line - top_line )
		self.top_line = top_line
		self.bot_line = self.top_line + self.win_height
		self.lines = self.diffmodel.get_lines( self.top_line, self.bot_line )

	def main_loop( self ):

		keep_going = True
		while keep_going:
			key = self.stdscr.getch()
			keep_going = self.process_keypress( key )

	def process_keypress( self, key, wait_for_input=True ):

		status_line = -1

		keep_going = True

		if key == ord( "q" ): # Quit
			keep_going = False
		elif key == ord( "h" ) or key == curses.KEY_LEFT:
			status_line = self.move_cursor( NCursesView.LEFT, False )
		elif key == ord( "l" ) or key == curses.KEY_RIGHT:
			status_line = self.move_cursor( NCursesView.RIGHT, False )
		elif key == ord( "j" ) or key == curses.KEY_DOWN:
			status_line = self.move_cursor( NCursesView.DOWN, False )
		elif key == ord( "k" ) or key == curses.KEY_UP:
			status_line = self.move_cursor( NCursesView.UP, False )
		elif key == ord( "J" ): # Extend selection down
			status_line = self.move_cursor( NCursesView.DOWN, True )
		elif key == ord( "K" ): # Extend selection up
			status_line = self.move_cursor( NCursesView.UP, True )
		elif key == ord( "." ) or key == curses.KEY_NPAGE: # Page down
			status_line = self.change_page( 1, False )
		elif key == ord( "," ) or key == curses.KEY_PPAGE: # Page up
			status_line = self.change_page( -1, False )
		elif key == ord( ">" ): # Extend selection 1 page down
			status_line = self.change_page( 1, True )
		elif key == ord( "<" ): # Extend selection 1 page up
			status_line = self.change_page( -1, True )
		elif key == ord( "n" ) or key == curses.KEY_F8: # Next difference
			status_line = self.next_difference( 1 )
		elif key == ord( "p" ) or key == curses.KEY_F7: # Previous difference
			status_line = self.next_difference( -1 )
		elif key == ord( "z" ): # Scroll left
			status_line = self.scroll_horizontal( -1 )
		elif key == ord( "x" ): # Scroll right
			status_line = self.scroll_horizontal( 1 )
		elif key == ord( "H" ): # Help
			status_line = self.show_help( wait_for_input )

		if status_line is None:
			self.set_status_line( DEFAULT_STATUS_MESSAGE, False )
		elif status_line == -1:
			pass # An unused key was pressed
		else:
			self.set_status_line( status_line )

		return keep_going

	def show_help( self, wait_for_input ):
		self.set_status_line( _("Press any key to continue"), False )

		self.textwindow.erase()

		line_num = self.win_height - 4
		for line in COPYRIGHT_MESSAGES:
			self.textwindow.addnstr( line_num, 0,
				line, self.win_width, self.CP_NORMAL )
			line_num += 1

		for line_num, line in enumerate( HELP_MESSAGES ):
			if isinstance( line, str ):
				newline = line.center( self.win_width )
			else:
				newline = "%%0%ds - %%s" % ( self.win_width // 2 )
				newline = newline % ( line[0], line[1] )
			self.textwindow.addnstr( line_num, 0,
				newline, self.win_width, self.CP_NORMAL )

		self.textwindow.refresh()
		if wait_for_input:
			self.textwindow.getch()
			self.set_status_line( DEFAULT_STATUS_MESSAGE, False )
			self.draw_screen()

	def get_horizontal_scroll_width( self ):
		return 5

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

	def move_cursor( self, dr, shift_pressed ):
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
					# Move the cursor 0 lines - resets selection if
					# shift is not pressed
					self.mycursor.add_to_line_num( 0, shift_pressed )
					redraw = True
			else:
				self.add_to_cursor_and_refresh( -1, shift_pressed )
		elif dr == NCursesView.DOWN:
			num_model_lines = self.diffmodel.get_num_lines()
			if self.mycursor.line_num == ( self.win_height - 1 ):
				if self.bot_line < num_model_lines:
					self.set_top_line( self.top_line + 1 )
					# Move the cursor 0 lines - resets selection if
					# shift is not pressed
					self.mycursor.add_to_line_num( 0, shift_pressed )
					redraw = True
			elif self.mycursor.line_num + self.top_line == num_model_lines - 1:
				pass # We are at the bottom of the diff.  Don't move down.
			else:
				self.add_to_cursor_and_refresh( 1, shift_pressed )
		if redraw:
			self.draw_screen()

	def add_to_cursor_and_refresh( self, direction, shift_pressed ):
		old_range = self.mycursor.get_selected_range()
		self.mycursor.add_to_line_num( direction, shift_pressed )
		new_range = self.mycursor.get_selected_range()
		# Use set union here to avoid updating a line twice
		for line_num in set( old_range ).union( new_range ):
			self.draw_single_line_if_visible( line_num )
		self.textwindow.refresh()

	def move_cursor_and_refresh( self, line_num, shift_pressed ):
		self.add_to_cursor_and_refresh(
			line_num - self.mycursor.line_num, shift_pressed )

	def refresh_cursor_line( self ):
		self.add_to_cursor_and_refresh( 0, False )

	def change_page( self, direction, shift_pressed ):
		top_line = self.top_line
		top_line += direction * self.win_height
		if top_line > self.diffmodel.get_num_lines() - self.win_height:
			top_line = self.diffmodel.get_num_lines() - self.win_height
		if top_line < 0:
			top_line = 0

		redraw = False
		if top_line != self.top_line:
			# Normal case - move up/down a page and put the cursor in the same
			# screen position.
			self.set_top_line( top_line )
			# Move the cursor zero lines, so if we are not extending
			# the selection, we reset to selecting only one line.
			self.mycursor.add_to_line_num( 0, shift_pressed )
			redraw = True
		elif top_line == 0 and self.mycursor.line_num != 0 and direction < 0:
			# We hit the top - move the cursor up to the top
			self.move_cursor_and_refresh( 0, shift_pressed )
		elif ( self.bot_line == self.diffmodel.get_num_lines() and
				self.mycursor.line_num != self.win_height - 1 ):
			# We hit the bottom - move the cursor down to the bottom
			self.move_cursor_and_refresh( self.win_height - 1, shift_pressed )
		elif ( direction > 0 and
				self.diffmodel.get_num_lines() - self.top_line
					< self.win_height ):
			self.move_cursor_and_refresh( self.diffmodel.get_num_lines()
				- self.top_line - 1, shift_pressed )

		if redraw:
			while self.scrolled_off_right():
				self.first_col -= self.get_horizontal_scroll_width()
				if self.first_col < 0:
					self.first_col = 0

			self.draw_screen()

	def get_line_of_next_diff( self, direction ):
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

		return line, current_pos

	def get_line_of_end_of_diff( self, direction, line, current_pos ):
		"""If we're going forwards, find out whether we need
		to scroll or not.  If we're going backwards, find
		the beginning of this difference (that is where
		the cursor is going to be)."""

		next_line_pos = current_pos
		next_line = line
		while( next_line is not None and
			   next_line.status != difflinetypes.IDENTICAL ):
			if next_line_pos >= ( self.bot_line - 1 ):
				# If we've gone off the bottom, there's no point
				# going on - we definitely need to scroll
				next_line_pos += direction # Add this as it's
				                           # about to be minused
				break
			next_line_pos += direction
			next_line = self.diffmodel.get_line( next_line_pos )

		next_line_pos -= direction

		return next_line_pos

	def scroll_to_line( self, current_pos ):
		old_top_line = self.top_line
		top_line = current_pos - NEXT_DIFF_MARGIN
		curs_pos = NEXT_DIFF_MARGIN

		max_top_line = self.diffmodel.get_num_lines() - self.win_height
		if top_line > max_top_line:
			adjustment = max_top_line - top_line
			top_line += adjustment
			curs_pos -= adjustment

		if top_line < 0:
			curs_pos += top_line
			top_line = 0

		if old_top_line != top_line:
			# Normal case - we have scrolled
			self.set_top_line( top_line )
			self.mycursor.set_line_num( curs_pos, False )
			self.draw_screen()
		else:
			# If we didn't scroll at all, just move cursor
			self.move_cursor_and_refresh( curs_pos, False )

	def next_difference( self, direction ):

		line, current_pos = self.get_line_of_next_diff( direction )

		# If there are no more differences, we have
		# nothing to do
		if line is None:
			this_line_status = self.lines[self.mycursor.line_num].status
			if direction > 0:
				if this_line_status == difflinetypes.IDENTICAL:
					return _("After last difference")
				else:
					return _("At last difference")
			else:
				if this_line_status == difflinetypes.IDENTICAL:
					return _("Before first difference")
				else:
					return _("At first difference")

		next_line_pos = self.get_line_of_end_of_diff(
			direction, line, current_pos )

		if direction < 0:
			# If we're going backwards, we jump to the
			# beginning of this difference
			current_pos = next_line_pos
			if current_pos <= self.top_line:
				scroll = True
			else:
				scroll = False
		else:
			if next_line_pos >= ( self.bot_line - 1 ):
				scroll = True
			else:
				scroll = False

		if scroll:
			self.scroll_to_line( current_pos )
		else:
			self.move_cursor_and_refresh( current_pos - self.top_line, False )


	def make_color_pairs( self ):
		curses.use_default_colors()

		self.CP_NORMAL = self.create_color_pair(
			1, -1, -1)
		self.CP_DIFFERENT  = self.create_color_pair(
			2, curses.COLOR_YELLOW,  -1 )
		self.CP_ADD = self.create_color_pair(
			3, curses.COLOR_GREEN, -1 )
		self.CP_REMOVE = self.create_color_pair(
			4, curses.COLOR_RED, -1 )
		self.CP_MISSING = self.create_color_pair(
			5, curses.COLOR_MAGENTA, -1 )

	def create_color_pair( self, pair_num, fore, back ):
		curses.init_pair( pair_num, fore, back )
		return curses.color_pair( pair_num )

	def format_filename( self, filename, width ):
		if filename is None:
			return ""
		elif len( filename ) > width:
			return "..." + filename[len(filename)-(width-3):]
		else:
			return filename

	def draw_header_window( self ):
		left  = self.format_filename( self.filename1, self.left_width )
		right = self.format_filename( self.filename2, self.right_width )

		self.headerwindow.addnstr( 0, 0,
			left, self.left_width )
		self.headerwindow.addnstr( 0, self.right_start,
			right, self.right_width )

		self.headerwindow.refresh()

	def set_status_line( self, message, special=True ):
		if special:
			colour = self.CP_MISSING | curses.A_REVERSE
		else:
			colour = self.CP_NORMAL | curses.A_REVERSE
		message = message.center( self.win_width )
		self.statuswindow.addnstr( 0, 0, message, self.win_width, colour )
		self.statuswindow.refresh()

	def draw_screen( self ):
		self.textwindow.erase()

		for line_num, ln in enumerate( self.lines ):
			self.write_line( ln, line_num )

		self.textwindow.refresh()

	def draw_single_line_if_visible( self, line_num ):
		if 0 <= line_num < len( self.lines ) :
			self.write_line( self.lines[line_num], line_num )

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

		if self.mycursor.is_line_selected( line_num ):
			if self.mycursor.lr == NCursesView.LEFT:
				left_colour_pair  |= curses.A_REVERSE
			else:
				right_colour_pair |= curses.A_REVERSE

		left  = self.pad_to_width( ln.left, self.first_col, self.left_width )
		right = self.pad_to_width( ln.right, self.first_col, self.right_width )

		self.textwindow.addnstr( line_num, 0, left, self.left_width,
			left_colour_pair )
		self.textwindow.addnstr( line_num, self.right_start, right,
			self.right_width, right_colour_pair )
		self.textwindow.addnstr( line_num, self.mid_col,
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

	def build_screenshot( self, window ):
		height, width = window.getmaxyx()
		width -= 1
		ret = ""
		prev_attr = -1
		for y in xrange( height ):
			for x in xrange( width ):
				ch_plus_attrs = window.inch( y, x )
				ch = chr( ch_plus_attrs & 0xFF )
				attr = ch_plus_attrs >> 8
				if attr != prev_attr:
					prev_attr = attr
					ret += self.attr_to_string( attr )
				ret += ch
			ret += "\n"
		return ret

	def screenshot_textwindow( self ):
		return self.build_screenshot( self.textwindow )

	def screenshot_header( self ):
		return self.build_screenshot( self.headerwindow )

	def screenshot_status( self ):
		return self.build_screenshot( self.statuswindow )

