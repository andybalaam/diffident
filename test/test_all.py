import test_listview
import test_diffmodel

def test_all():
	test_listview.run()
	test_diffmodel.run()

	print "All tests passed."

	return 0

