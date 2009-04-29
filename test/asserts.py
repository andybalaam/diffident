
def assert_strings_equal( str1, str2 ):
	if str1 == str2:
		return

	str1 = str1.replace( " ", "." )
	str2 = str2.replace( " ", "." )

	print str1 + "\n!= \n" + str2

	char = None
	for i in xrange( min( len( str1 ),
			len( str2 ) ) ):
		if str1[i] != str2[i]:
			char = i
			break

	if char is None:
		if len( str1 ) > len( str2 ):
			print "The first one is longer."
		else:
			print "The second one is longer."
	else:
		print "At character %d, %s != %s" % (
			char, str1[char], str2[char] )

	raise AssertionError()

