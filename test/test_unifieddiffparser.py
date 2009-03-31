from asserts import assert_strings_equal

from lib.unifieddiffparser import UnifiedDiffParser
from lib.diffmodel import DiffModel
import lib.difflinetypes as difflinetypes

def parse_hunks():
	diffparser = UnifiedDiffParser( None, None );
	assert( diffparser.parse_hunk_line( "@@ -1,2 +1,2 @@" ) == 1 )
	assert( diffparser.parse_hunk_line( "@@ -36,5 +36,5 @@" ) == 36 )

def just_differences():
	file1 = [
		"line 1 here",
		"line 2 here",
	]

	diff = [
		"--- test/file1.txt	2009-03-22 21:42:38.000000000 +0000",
		"+++ test/file2.txt	2009-03-22 21:53:26.000000000 +0000",
		"@@ -1,2 +1,2 @@",
		"-line 1 here",
		"-line 2 here",
		"+line 1 here different",
		"+line 2 here different",
	]

	unifieddiffparser = UnifiedDiffParser( file1, diff )
	diffmodel = DiffModel( unifieddiffparser )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left,  "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here different" )
	assert( lines[0].status == difflinetypes.DIFFERENT )

	assert_strings_equal( lines[1].left,  "line 2 here" )
	assert_strings_equal( lines[1].right, "line 2 here different" )
	assert( lines[1].status == difflinetypes.DIFFERENT )

def identical():
	file1 = [
		"line 1 here",
		"line 2 here",
	]

	diff = []

	unifieddiffparser = UnifiedDiffParser( file1, diff )
	diffmodel = DiffModel( unifieddiffparser )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left,  "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here" )
	assert( lines[0].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[1].left,  "line 2 here" )
	assert_strings_equal( lines[1].right, "line 2 here" )
	assert( lines[1].status == difflinetypes.IDENTICAL )


def diff_then_same():
	file1 = [
		"line 1 here",
		"line 2 here",
		"line 3 here",
		"line 4 here",
	]

	diff = [
		"--- test/file1.txt	2009-03-27 21:06:15.000000000 +0000",
		"+++ test/file2.txt	2009-03-27 21:11:54.000000000 +0000",
		"@@ -1,4 +1,4 @@",
		"-line 1 here",
		"-line 2 here",
		"+line 1 here different",
		"+line 2 here different",
		" line 3 here",
		" line 4 here",
	]

	unifieddiffparser = UnifiedDiffParser( file1, diff )
	diffmodel = DiffModel( unifieddiffparser )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left,  "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here different" )
	assert( lines[0].status == difflinetypes.DIFFERENT )

	assert_strings_equal( lines[1].left,  "line 2 here" )
	assert_strings_equal( lines[1].right, "line 2 here different" )
	assert( lines[1].status == difflinetypes.DIFFERENT )

	assert_strings_equal( lines[2].left,  "line 3 here" )
	assert_strings_equal( lines[2].right, "line 3 here" )
	assert( lines[2].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[3].left,  "line 4 here" )
	assert_strings_equal( lines[3].right, "line 4 here" )
	assert( lines[3].status == difflinetypes.IDENTICAL )


def same_then_diff():
	file1 = [
		"line 1 here",
		"line 2 here",
		"line 3 here",
		"line 4 here",
	]

	diff = [
		"--- test/file1.txt	2009-03-27 21:06:15.000000000 +0000",
		"+++ test/file2.txt	2009-03-27 21:19:51.000000000 +0000",
		"@@ -1,4 +1,4 @@",
		" line 1 here",
		" line 2 here",
		"-line 3 here",
		"-line 4 here",
		"+line 3 here different",
		"+line 4 here different",
	]

	unifieddiffparser = UnifiedDiffParser( file1, diff )
	diffmodel = DiffModel( unifieddiffparser )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left,  "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here" )
	assert( lines[0].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[1].left,  "line 2 here" )
	assert_strings_equal( lines[1].right, "line 2 here" )
	assert( lines[1].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[2].left,  "line 3 here" )
	assert_strings_equal( lines[2].right, "line 3 here different" )
	assert( lines[2].status == difflinetypes.DIFFERENT )

	assert_strings_equal( lines[3].left,  "line 4 here" )
	assert_strings_equal( lines[3].right, "line 4 here different" )
	assert( lines[3].status == difflinetypes.DIFFERENT )

def multiple_hunks_no_deletions_or_additions():
	file1 = []
	for i in range( 1, 41 ):
		file1.append( "line %d here" % i )

	diff = [
		"--- test/file1.txt	2009-03-28 00:34:14.000000000 +0000",
		"+++ test/file2.txt	2009-03-28 00:34:33.000000000 +0000",
		"@@ -1,5 +1,5 @@",
		" line 1 here",
		"-line 2 here",
		"+line 2 here different",
		" line 3 here",
		" line 4 here",
		" line 5 here",
		"@@ -36,5 +36,5 @@",
		" line 36 here",
		" line 37 here",
		" line 38 here",
		"-line 39 here",
		"+line 39 here different",
		" line 40 here",
	]

	unifieddiffparser = UnifiedDiffParser( file1, diff )
	diffmodel = DiffModel( unifieddiffparser )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left,  "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here" )
	assert( lines[0].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[1].left,  "line 2 here" )
	assert_strings_equal( lines[1].right, "line 2 here different" )
	assert( lines[1].status == difflinetypes.DIFFERENT )

	for i in range( 3, 39 ):
		assert_strings_equal( lines[i-1].left,  "line %d here" % i )
		assert_strings_equal( lines[i-1].right, "line %d here" % i )
		assert( lines[i-1].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[38].left,  "line 39 here" )
	assert_strings_equal( lines[38].right, "line 39 here different" )
	assert( lines[38].status == difflinetypes.DIFFERENT )

	assert_strings_equal( lines[39].left,  "line 40 here" )
	assert_strings_equal( lines[39].right, "line 40 here" )
	assert( lines[39].status == difflinetypes.IDENTICAL )

def added_at_end():

	file1 = [
		"line 1 here",
		"line 2 here",
	]

	diff = [
		"--- test/file1.txt	2009-03-28 15:18:52.000000000 +0000",
		"+++ test/file2.txt	2009-03-28 15:19:28.000000000 +0000",
		"@@ -1,2 +1,4 @@",
		" line 1 here",
		" line 2 here",
		"+line 3 here",
		"+line 4 here",
	]

	unifieddiffparser = UnifiedDiffParser( file1, diff )
	diffmodel = DiffModel( unifieddiffparser )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left,  "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here" )
	assert( lines[0].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[1].left,  "line 2 here" )
	assert_strings_equal( lines[1].right, "line 2 here" )
	assert( lines[1].status == difflinetypes.IDENTICAL )

	assert( lines[2].left is None )
	assert_strings_equal( lines[2].right, "line 3 here" )
	assert( lines[2].status == difflinetypes.ADD )

	assert( lines[3].left is None )
	assert_strings_equal( lines[3].right, "line 4 here" )
	assert( lines[3].status == difflinetypes.ADD )

def added_in_middle():

	file1 = [
		"line 1 here",
		"line 3 here",
		"line 4 here",
		"line 5 here",
		"line 6 here",
		"line 7 here",
		"line 8 here",
		"line 9 here",
		"line 10 here",
		"line 11 here",
		"line 12 here",
		"line 13 here",
		"line 14 here",
		"line 16 here",
	]

	diff = [
		"--- test/file1.txt	2009-03-28 15:28:21.000000000 +0000",
		"+++ test/file2.txt	2009-03-28 15:27:50.000000000 +0000",
		"@@ -1,4 +1,5 @@",
		" line 1 here",
		"+line 2 here",
		" line 3 here",
		" line 4 here",
		" line 5 here",
		"@@ -11,4 +12,5 @@",
		" line 12 here",
		" line 13 here",
		" line 14 here",
		"+line 15 here",
		" line 16 here",
	]

	unifieddiffparser = UnifiedDiffParser( file1, diff )
	diffmodel = DiffModel( unifieddiffparser )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left,  "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here" )
	assert( lines[0].status == difflinetypes.IDENTICAL )

	assert( lines[1].left is None )
	assert_strings_equal( lines[1].right, "line 2 here" )
	assert( lines[1].status == difflinetypes.ADD )

	for i in range( 3, 15 ):
		assert_strings_equal( lines[i-1].left,  "line %d here" % i )
		assert_strings_equal( lines[i-1].right, "line %d here" % i )
		assert( lines[i-1].status == difflinetypes.IDENTICAL )

	assert( lines[14].left is None )
	assert_strings_equal( lines[14].right, "line 15 here" )
	assert( lines[14].status == difflinetypes.ADD )

	assert_strings_equal( lines[15].left, "line 16 here" )
	assert_strings_equal( lines[15].right, "line 16 here" )
	assert( lines[15].status == difflinetypes.IDENTICAL )

def added_at_beginning():

	file1 = [
		"line 3 here",
		"line 4 here",
	]

	diff = [
		"--- test/file1.txt	2009-03-28 15:33:40.000000000 +0000",
		"+++ test/file2.txt	2009-03-28 15:33:45.000000000 +0000",
		"@@ -1,2 +1,4 @@",
		"+line 1 here",
		"+line 2 here",
		" line 3 here",
		" line 4 here",
	]

	unifieddiffparser = UnifiedDiffParser( file1, diff )
	diffmodel = DiffModel( unifieddiffparser )

	lines = diffmodel.get_lines()

	assert( lines[0].left is None )
	assert_strings_equal( lines[0].right, "line 1 here" )
	assert( lines[0].status == difflinetypes.ADD )

	assert( lines[1].left is None )
	assert_strings_equal( lines[1].right, "line 2 here" )
	assert( lines[1].status == difflinetypes.ADD )

	assert_strings_equal( lines[2].left, "line 3 here" )
	assert_strings_equal( lines[2].right, "line 3 here" )
	assert( lines[2].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[3].left, "line 4 here" )
	assert_strings_equal( lines[3].right, "line 4 here" )
	assert( lines[3].status == difflinetypes.IDENTICAL )

def removed_at_end():

	file1 = [
		"line 1 here",
		"line 2 here",
		"line 3 here",
		"line 4 here",
	]

	diff = [
		"--- test/file1.txt	2009-03-28 15:39:09.000000000 +0000",
		"+++ test/file2.txt	2009-03-28 15:39:12.000000000 +0000",
		"@@ -1,4 +1,2 @@",
		" line 1 here",
		" line 2 here",
		"-line 3 here",
		"-line 4 here",
	]

	unifieddiffparser = UnifiedDiffParser( file1, diff )
	diffmodel = DiffModel( unifieddiffparser )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left,  "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here" )
	assert( lines[0].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[1].left,  "line 2 here" )
	assert_strings_equal( lines[1].right, "line 2 here" )
	assert( lines[1].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[2].left, "line 3 here" )
	assert( lines[2].right is None )
	assert( lines[2].status == difflinetypes.REMOVE )

	assert_strings_equal( lines[3].left, "line 4 here" )
	assert( lines[3].right is None )
	assert( lines[3].status == difflinetypes.REMOVE )

def removed_in_middle():

	file1 = [
		"line 1 here",
		"line 2 here",
		"line 3 here",
		"line 4 here",
		"line 5 here",
		"line 6 here",
		"line 7 here",
		"line 8 here",
		"line 9 here",
		"line 10 here",
		"line 11 here",
		"line 12 here",
		"line 13 here",
		"line 14 here",
		"line 15 here",
		"line 16 here",
	]

	diff = [
		"--- test/file1.txt	2009-03-28 20:29:28.000000000 +0000",
		"+++ test/file2.txt	2009-03-28 20:29:37.000000000 +0000",
		"@@ -1,5 +1,4 @@",
		" line 1 here",
		"-line 2 here",
		" line 3 here",
		" line 4 here",
		" line 5 here",
		"@@ -12,5 +11,4 @@",
		" line 12 here",
		" line 13 here",
		" line 14 here",
		"-line 15 here",
		" line 16 here",
	]

	unifieddiffparser = UnifiedDiffParser( file1, diff )
	diffmodel = DiffModel( unifieddiffparser )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left,  "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here" )
	assert( lines[0].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[1].left, "line 2 here" )
	assert( lines[1].right is None )
	assert( lines[1].status == difflinetypes.REMOVE )

	for i in range( 3, 15 ):
		assert_strings_equal( lines[i-1].left,  "line %d here" % i )
		assert_strings_equal( lines[i-1].right, "line %d here" % i )
		assert( lines[i-1].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[14].left, "line 15 here" )
	assert( lines[14].right is None )
	assert( lines[14].status == difflinetypes.REMOVE )

	assert_strings_equal( lines[15].left, "line 16 here" )
	assert_strings_equal( lines[15].right, "line 16 here" )
	assert( lines[15].status == difflinetypes.IDENTICAL )

def removed_at_beginning():

	file1 = [
		"line 1 here",
		"line 2 here",
		"line 3 here",
		"line 4 here",
	]

	diff = [
		"--- test/file1.txt	2009-03-28 20:32:36.000000000 +0000",
		"+++ test/file2.txt	2009-03-28 20:32:41.000000000 +0000",
		"@@ -1,4 +1,2 @@",
		"-line 1 here",
		"-line 2 here",
		" line 3 here",
		" line 4 here",
	]

	unifieddiffparser = UnifiedDiffParser( file1, diff )
	diffmodel = DiffModel( unifieddiffparser )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left, "line 1 here" )
	assert( lines[0].right is None )
	assert( lines[0].status == difflinetypes.REMOVE )

	assert_strings_equal( lines[1].left, "line 2 here" )
	assert( lines[1].right is None )
	assert( lines[1].status == difflinetypes.REMOVE )

	assert_strings_equal( lines[2].left, "line 3 here" )
	assert_strings_equal( lines[2].right, "line 3 here" )
	assert( lines[2].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[3].left, "line 4 here" )
	assert_strings_equal( lines[3].right, "line 4 here" )
	assert( lines[3].status == difflinetypes.IDENTICAL )

def changed_added_removed():

	file1 = [
		"line 1 here",
		"line 2 here",
		"line 3 here",
		"line 4 here",
		"line 5 here",
		"line 7 here",
		"line 8 here",
		"line 9 here",
		"line 10 here",
	]

	diff = [
		"--- test/file1.txt	2009-03-28 20:37:54.000000000 +0000",
		"+++ test/file2.txt	2009-03-28 20:37:47.000000000 +0000",
		"@@ -1,9 +1,8 @@",
		" line 1 here",
		"-line 2 here",
		"-line 3 here",
		"+line 2 here different",
		" line 4 here",
		" line 5 here",
		"+line 6 here",
		" line 7 here",
		" line 8 here",
		"-line 9 here",
		" line 10 here",
	]

	unifieddiffparser = UnifiedDiffParser( file1, diff )
	diffmodel = DiffModel( unifieddiffparser )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left, "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here" )
	assert( lines[0].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[1].left, "line 2 here" )
	assert_strings_equal( lines[1].right, "line 2 here different" )
	assert( lines[1].status == difflinetypes.DIFFERENT )

	assert_strings_equal( lines[2].left, "line 3 here" )
	assert( lines[2].right is None )
	assert( lines[2].status == difflinetypes.REMOVE )

	assert_strings_equal( lines[3].left, "line 4 here" )
	assert_strings_equal( lines[3].right, "line 4 here" )
	assert( lines[3].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[4].left, "line 5 here" )
	assert_strings_equal( lines[4].right, "line 5 here" )
	assert( lines[4].status == difflinetypes.IDENTICAL )

	assert( lines[5].left is None )
	assert_strings_equal( lines[5].right, "line 6 here" )
	assert( lines[5].status == difflinetypes.ADD )

	assert_strings_equal( lines[6].left, "line 7 here" )
	assert_strings_equal( lines[6].right, "line 7 here" )
	assert( lines[6].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[7].left, "line 8 here" )
	assert_strings_equal( lines[7].right, "line 8 here" )
	assert( lines[7].status == difflinetypes.IDENTICAL )

	assert_strings_equal( lines[8].left, "line 9 here" )
	assert( lines[8].right is None )
	assert( lines[8].status == difflinetypes.REMOVE )

	assert_strings_equal( lines[9].left, "line 10 here" )
	assert_strings_equal( lines[9].right, "line 10 here" )
	assert( lines[9].status == difflinetypes.IDENTICAL )

def run():
	parse_hunks()

	just_differences()
	identical()
	diff_then_same()
	same_then_diff()
	multiple_hunks_no_deletions_or_additions()

	added_at_end()
	added_in_middle()
	added_at_beginning()

	removed_at_end()
	removed_in_middle()
	removed_at_beginning()

	changed_added_removed()

