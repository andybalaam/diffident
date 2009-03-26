
def assert_strings_equal( str1, str2 ):
	if str1 == str2:
		return

	print str1 + "\n!= \n" + str2

	raise AssertionError()

