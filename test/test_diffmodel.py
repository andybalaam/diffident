from lib.diffmodel import DiffModel
from asserts import assert_strings_equal

def parse_hunks():
	diffmodel = DiffModel( None, None, None );
	assert( diffmodel.parse_hunk_line( "@@ -1,2 +1,2 @@" ) == 1 )
	assert( diffmodel.parse_hunk_line( "@@ -36,5 +36,5 @@" ) == 36 )

def just_differences():
	file1 = [
		"line 1 here",
		"line 2 here",
	]

	file2 = [
		"line 1 here different",
		"line 2 here different",
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

	diffmodel = DiffModel( file1, file2, diff )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left,  "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here different" )
	assert( lines[0].status == DiffModel.DIFFERENT )

	assert_strings_equal( lines[1].left,  "line 2 here" )
	assert_strings_equal( lines[1].right, "line 2 here different" )
	assert( lines[1].status == DiffModel.DIFFERENT )

def identical():
	file1 = [
		"line 1 here",
		"line 2 here",
	]

	file2 = [
		"line 1 here",
		"line 2 here",
	]

	diff = []

	diffmodel = DiffModel( file1, file2, diff )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left,  "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here" )
	assert( lines[0].status == DiffModel.IDENTICAL )

	assert_strings_equal( lines[1].left,  "line 2 here" )
	assert_strings_equal( lines[1].right, "line 2 here" )
	assert( lines[1].status == DiffModel.IDENTICAL )


def diff_then_same():
	file1 = [
		"line 1 here",
		"line 2 here",
		"line 3 here",
		"line 4 here",
	]

	file2 = [
		"line 1 here different",
		"line 2 here different",
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

	diffmodel = DiffModel( file1, file2, diff )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left,  "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here different" )
	assert( lines[0].status == DiffModel.DIFFERENT )

	assert_strings_equal( lines[1].left,  "line 2 here" )
	assert_strings_equal( lines[1].right, "line 2 here different" )
	assert( lines[1].status == DiffModel.DIFFERENT )

	assert_strings_equal( lines[2].left,  "line 3 here" )
	assert_strings_equal( lines[2].right, "line 3 here" )
	assert( lines[2].status == DiffModel.IDENTICAL )

	assert_strings_equal( lines[3].left,  "line 4 here" )
	assert_strings_equal( lines[3].right, "line 4 here" )
	assert( lines[3].status == DiffModel.IDENTICAL )


def same_then_diff():
	file1 = [
		"line 1 here",
		"line 2 here",
		"line 3 here",
		"line 4 here",
	]

	file2 = [
		"line 1 here",
		"line 2 here",
		"line 3 here different",
		"line 4 here different",
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

	diffmodel = DiffModel( file1, file2, diff )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left,  "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here" )
	assert( lines[0].status == DiffModel.IDENTICAL )

	assert_strings_equal( lines[1].left,  "line 2 here" )
	assert_strings_equal( lines[1].right, "line 2 here" )
	assert( lines[1].status == DiffModel.IDENTICAL )

	assert_strings_equal( lines[2].left,  "line 3 here" )
	assert_strings_equal( lines[2].right, "line 3 here different" )
	assert( lines[2].status == DiffModel.DIFFERENT )

	assert_strings_equal( lines[3].left,  "line 4 here" )
	assert_strings_equal( lines[3].right, "line 4 here different" )
	assert( lines[3].status == DiffModel.DIFFERENT )

def multiple_hunks_no_deletions_or_additions():
	file1 = []
	for i in range( 1, 41 ):
		file1.append( "line %d here" % i )

	file2 = []
	for line in file1:
		file2.append( line )

	for i in ( 2, 39 ):
		file2[i-1] += " different"

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

	diffmodel = DiffModel( file1, file2, diff )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left,  "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here" )
	assert( lines[0].status == DiffModel.IDENTICAL )

	assert_strings_equal( lines[1].left,  "line 2 here" )
	assert_strings_equal( lines[1].right, "line 2 here different" )
	assert( lines[1].status == DiffModel.DIFFERENT )

	for i in range( 3, 39 ):
		assert_strings_equal( lines[i-1].left,  "line %d here" % i )
		assert_strings_equal( lines[i-1].right, "line %d here" % i )
		assert( lines[i-1].status == DiffModel.IDENTICAL )

	assert_strings_equal( lines[38].left,  "line 39 here" )
	assert_strings_equal( lines[38].right, "line 39 here different" )
	assert( lines[38].status == DiffModel.DIFFERENT )

	assert_strings_equal( lines[39].left,  "line 40 here" )
	assert_strings_equal( lines[39].right, "line 40 here" )
	assert( lines[39].status == DiffModel.IDENTICAL )

def added_at_end():

	file1 = [
		"line 1 here",
		"line 2 here",
	]

	file2 = [
		"line 1 here",
		"line 2 here",
		"line 3 here",
		"line 4 here",
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

	diffmodel = DiffModel( file1, file2, diff )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left,  "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here" )
	assert( lines[0].status == DiffModel.IDENTICAL )

	assert_strings_equal( lines[1].left,  "line 2 here" )
	assert_strings_equal( lines[1].right, "line 2 here" )
	assert( lines[1].status == DiffModel.IDENTICAL )

	assert( lines[2].left is None )
	assert_strings_equal( lines[2].right, "line 3 here" )
	assert( lines[2].status == DiffModel.ADD )

	assert( lines[3].left is None )
	assert_strings_equal( lines[3].right, "line 4 here" )
	assert( lines[3].status == DiffModel.ADD )

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

	file2 = [
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

	diffmodel = DiffModel( file1, file2, diff )

	lines = diffmodel.get_lines()

	assert_strings_equal( lines[0].left,  "line 1 here" )
	assert_strings_equal( lines[0].right, "line 1 here" )
	assert( lines[0].status == DiffModel.IDENTICAL )

	assert( lines[1].left is None )
	assert_strings_equal( lines[1].right, "line 2 here" )
	assert( lines[1].status == DiffModel.ADD )

	for i in range( 3, 15 ):
		assert_strings_equal( lines[i-1].left,  "line %d here" % i )
		assert_strings_equal( lines[i-1].right, "line %d here" % i )
		assert( lines[i-1].status == DiffModel.IDENTICAL )

	assert( lines[14].left is None )
	assert_strings_equal( lines[14].right, "line 15 here" )
	assert( lines[14].status == DiffModel.ADD )

	assert_strings_equal( lines[15].left, "line 16 here" )
	assert_strings_equal( lines[15].right, "line 16 here" )
	assert( lines[15].status == DiffModel.IDENTICAL )

def run():
	parse_hunks()

	just_differences()
	identical()
	diff_then_same()
	same_then_diff()
	multiple_hunks_no_deletions_or_additions()
	added_at_end()
	added_in_middle()

