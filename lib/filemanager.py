
from lib.constants import directions
from lib.constants import save_status

class FileManager( object ):
	def __init__( self, filename_left, filename_right ):
		self.filenames = {
			directions.LEFT  : filename_left,
			directions.RIGHT : filename_right,
			}

	def save( self, editablediffmodel, side ):
		if not editablediffmodel.has_edit_affecting_side( side ):
			return save_status.STATUS_NOCHANGES

		fl = open( self.filenames[side], "w" )
		status = editablediffmodel.write_to_file( fl, side )
		fl.close()

		return save_status.STATUS_SAVED


