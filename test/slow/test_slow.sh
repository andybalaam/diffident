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
	cat >file1.tmptxt <<END
blah
blah
blah
END

	cat >file2.tmptxt <<END
blah
blah
blah
END

	./diffident.py file1.tmptxt file2.tmptxt > output-diffident.tmptxt

	diff --side-by-side --width=80 --expand-tabs file1.tmptxt file2.tmptxt > output-diff.tmptxt

	diff output-diffident.tmptxt output-diff.tmptxt > /dev/null
	assert_retval_is_zero $? listview_matches_diff

	#rm *.tmptxt
}

listview_matches_diff

