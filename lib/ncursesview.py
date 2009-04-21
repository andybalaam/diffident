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
		self.top_line = 0
		self.mycursor = NCursesView.Cursor( NCursesView.LEFT, 0 )

	def show( self ):
		curses.wrapper( self.show_impl )

	def show_impl( self, stdscr ):
		self.stdscr = stdscr

		curses.curs_set( 0 )

		self.make_color_pairs()

		( win_height, win_width ) = self.stdscr.getmaxyx()

		self.bot_line = self.top_line + win_height

		self.left_width  = ( win_width - 3 ) / 2
		self.right_width = self.left_width
		self.mid_col     = self.left_width + 1
		self.right_start = self.left_width + 3

		self.stdscr.bkgd( ord( " " ), self.BLACK )

		#self.lines = self.diffmodel.get_lines( self.bot_line, self.top_line )
		self.lines = self.diffmodel.get_lines()

		self.draw_screen()

		self.main_loop()

	def main_loop( self ):

		keep_going = True
		while keep_going:
			key = self.stdscr.getch()

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

	def move_cursor( self, dr ):
		if dr == NCursesView.LEFT and self.mycursor.lr == NCursesView.RIGHT:
			self.mycursor.lr = NCursesView.LEFT
			self.draw_screen()
		elif dr == NCursesView.RIGHT and self.mycursor.lr == NCursesView.LEFT:
			self.mycursor.lr = NCursesView.RIGHT
			self.draw_screen()
		elif dr == NCursesView.UP and self.mycursor.line_num > 0:
			self.mycursor.line_num -= 1
			self.draw_screen()
		elif dr == NCursesView.DOWN and (
				self.mycursor.line_num < ( self.bot_line - 1 ) ):
			self.mycursor.line_num += 1
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
			self.draw_line( ln, line_num )

		self.stdscr.refresh()

	def draw_line( self, ln, line_num ):

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

		left  = self.spaces_if_none( ln.left, self.left_width )
		right = self.spaces_if_none( ln.right, self.right_width )

		self.stdscr.addnstr( line_num, 0, left, self.left_width,
			left_colour_pair )
		self.stdscr.addnstr( line_num, self.right_start, right,
			self.right_width, right_colour_pair )
		self.stdscr.addch( line_num, self.mid_col, mid_char )

	def spaces_if_none( self, string, width ):
		if string is None:
			return " " * width
		else:
			return string


