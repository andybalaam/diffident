#!/usr/bin/python

from lib.diffmodel import DiffModel
from lib.listview import ListView

def test_2_different():
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

	listview = ListView( diffmodel )

	listview.set_columns( 80 )

	assert( listview.get_string() ==
"""line 1 here                            <> line 1 here different                 
line 2 here                            <> line 2 here different                 
""" )


def test_all():
	test_2_different()

if __name__ == "__main__":
	test_all()


