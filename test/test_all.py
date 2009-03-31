import test_listview
import test_diffmodel
import test_unifieddiffparser

def test_all():
	test_listview.run()
	test_diffmodel.run()
	test_unifieddiffparser.run()

	print "All tests passed."

	return 0

