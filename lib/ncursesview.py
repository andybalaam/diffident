import curses

import difflinetypes

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

		self.set_top_line( 0 )

		win_width_without_mid_col = self.win_width - 3
		self.left_width  = win_width_without_mid_col // 2
		self.right_width = win_width_without_mid_col - self.left_width
		self.mid_col     = self.left_width + 1
		self.right_start = self.left_width + 3

		self.stdscr.bkgd( ord( " " ), self.BLACK )

		#self.lines = self.diffmodel.get_lines( self.bot_line, self.top_line )
		self.lines = self.diffmodel.get_lines()

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

	def main_loop( self ):

		keep_going = True
		while keep_going:
			key = self.stdscr.getch()
			keep_going = self.process_keypress( key )

	def process_keypress( self, key ):
		keep_going = True
		if key == ord( "q" ):
			keep_going = False
		elif key == ord( "h" ) or key == curses.KEY_LEFT:
			self.move_cursor( NCursesView.LEFT )
		elif key == ord( "l" ) or key == curses.KEY_RIGHT:
			self.move_cursor( NCursesView.RIGHT )
		elif key == ord( "j" ) or key == curses.KEY_DOWN:
			self.move_cursor( NCursesView.DOWN )
		elif key == ord( "k" ) or key == curses.KEY_UP:
			self.move_cursor( NCursesView.UP )
		elif key == curses.KEY_NPAGE:
			self.change_page( 1 )
		elif key == curses.KEY_PPAGE:
			self.change_page( -1 )
		return keep_going

	def move_cursor( self, dr ):
		# TODO: don't redraw whole screen when scrolling?

		redraw = False

		if dr == NCursesView.LEFT and self.mycursor.lr == NCursesView.RIGHT:
			self.mycursor.lr = NCursesView.LEFT
			redraw = True
		elif dr == NCursesView.RIGHT and self.mycursor.lr == NCursesView.LEFT:
			self.mycursor.lr = NCursesView.RIGHT
			redraw = True
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
			self.draw_screen()

	def make_color_pairs( self ):
		curses.use_default_colors()

		self.BLACK = self.create_color_pair( 1, curses.COLOR_BLACK, -1 )
		self.CYAN  = self.create_color_pair( 2, curses.COLOR_CYAN,  -1 )
		self.GREEN = self.create_color_pair( 3, curses.COLOR_GREEN, -1 )
		self.RED   = self.create_color_pair( 4, curses.COLOR_RED,   -1 )

		self.BLACK_ON_WHITE = self.create_color_pair( 5, curses.COLOR_BLACK,
			curses.COLOR_WHITE )

	def create_color_pair( self, pair_num, fore, back ):
		curses.init_pair( pair_num, fore, back )
		return curses.color_pair( pair_num )

	def draw_screen( self ):
		self.stdscr.clear()

		#for ln in self.lines:
		for line_num, ln in enumerate( self.lines[
				self.top_line : self.bot_line ] ):
			self.write_line( ln, line_num )

		self.stdscr.refresh()

	def draw_single_line( self, line_num ):
		#ln = self.lines[line_num]
		ln = self.lines[self.top_line + line_num]
		self.write_line( ln, line_num )

	def write_line( self, ln, line_num ):

		if ln.status == difflinetypes.IDENTICAL:
			left_colour_pair  = self.BLACK
			right_colour_pair = self.BLACK
			mid_char = ord( " " )
		elif ln.status == difflinetypes.DIFFERENT:
			left_colour_pair  = self.CYAN
			right_colour_pair = self.CYAN
			mid_char = ord( "*" )
		elif ln.status == difflinetypes.ADD:
			left_colour_pair  = self.BLACK_ON_WHITE
			right_colour_pair = self.GREEN
			mid_char = ord( "+" )
		elif ln.status == difflinetypes.REMOVE:
			left_colour_pair  = self.RED
			right_colour_pair = self.BLACK_ON_WHITE
			mid_char = ord( "-" )
		else:
			raise Exception( "Unknown line type %d." % ln.status )

		if self.mycursor.line_num == line_num:
			if self.mycursor.lr == NCursesView.LEFT:
				left_colour_pair  |= curses.A_REVERSE
			else:
				right_colour_pair |= curses.A_REVERSE

		left  = self.pad_to_width( ln.left, self.left_width )
		right = self.pad_to_width( ln.right, self.right_width )

		self.stdscr.addnstr( line_num, 0, left, self.left_width,
			left_colour_pair )
		self.stdscr.addnstr( line_num, self.right_start, right,
			self.right_width, right_colour_pair )
		self.stdscr.addch( line_num, self.mid_col, mid_char )

	def pad_to_width( self, string, width ):
		if string is None:
			string = " "
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


