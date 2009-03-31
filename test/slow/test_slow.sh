#!/bin/bash

# Slow tests for diffident that run it through its command-line
# interface and make assertions about its behaviour.


function assert_retval_is_zero()
{
	if [ "$1" != "0" ]; then
	{
		echo "Return value was not zero in '$2'."
		exit 1
	}; fi
}

function listview_matches_diff()
{
	echo "$1" > file1.tmptxt
	echo "$2" > file2.tmptxt

	./diffident.py file1.tmptxt file2.tmptxt > output-diffident.tmptxt

	diff --side-by-side --width=80 --expand-tabs file1.tmptxt file2.tmptxt > output-diff.tmptxt

	diff output-diffident.tmptxt output-diff.tmptxt > /dev/null
	assert_retval_is_zero $? $3

	#rm *.tmptxt
}

function listview_matches_diff_nochanges()
{
	FILE1=`cat <<END
line 1
line 2
line 3

END`

	listview_matches_diff "$FILE1" "$FILE1" listview_matches_diff_nochanges
}


function listview_matches_diff_changes()
{
	FILE1=`cat <<END
line 1
line 2
line 3

END`

	FILE2=`cat <<END
line 1
line 2 changed
line 3
END`

	listview_matches_diff "$FILE1" "$FILE2" listview_matches_diff_changes
}

listview_matches_diff_nochanges
listview_matches_diff_changes
