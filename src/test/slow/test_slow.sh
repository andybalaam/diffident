#!/bin/bash

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

	./diffident.py --view=list file1.tmptxt file2.tmptxt > output-diffident.tmptxt
	assert_retval_is_zero $? $3-diffident

	diff --side-by-side --width=80 --expand-tabs file1.tmptxt file2.tmptxt > output-diff.tmptxt

	diff output-diffident.tmptxt output-diff.tmptxt > /dev/null
	assert_retval_is_zero $? $3-diff-outputs

	rm *.tmptxt
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


function listview_matches_diff_adds()
{
	FILE1=`cat <<END
line 1
line 3

END`

	FILE2=`cat <<END
line 1
line 2
line 3
END`

	listview_matches_diff "$FILE1" "$FILE2" listview_matches_diff_adds
}


function listview_matches_diff_removes()
{
	FILE1=`cat <<END
line 1
line 2
line 3

END`

	FILE2=`cat <<END
line 1
line 2
END`

	listview_matches_diff "$FILE1" "$FILE2" listview_matches_diff_removes
}

# Disabled since we show whole line and diff truncates.
#function listview_matches_diff_longline()
#{
#	FILE1=`cat <<END
#line 1
#12345678901234567890123456789012345678901234567890
#line 3
#
#END`
#
#	FILE2=`cat <<END
#line 1
#line 2
#line 3
#END`
#
#	listview_matches_diff "$FILE1" "$FILE2" listview_matches_diff_longline
#}

function ncursesview_saves_edits()
{
	FILE1=`cat <<END
left 1
left 2
left 3
END`

	FILE2=`cat <<END
right 1
right 2
right 3
END`

	EXPOUT=`cat <<END
left 1
right 2
right 3
END`

	echo "$FILE1" > file1.tmptxt
	echo "$FILE2" > file2.tmptxt
	echo "$EXPOUT" > expout.tmptxt

	./diffident.py --view=term --send-keys "]ls" file1.tmptxt file2.tmptxt
	assert_retval_is_zero $? ncursesview_saves_edits-diffident

	diff file2.tmptxt expout.tmptxt > /dev/null
	assert_retval_is_zero $? ncursesview_saves_edits-diff-outputs

	rm *.tmptxt
}

listview_matches_diff_nochanges
listview_matches_diff_changes
listview_matches_diff_adds
listview_matches_diff_removes

ncursesview_saves_edits

