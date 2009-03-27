from lib.diffmodel import DiffModel
from asserts import assert_strings_equal

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

def run():
	just_differences()
	identical()

