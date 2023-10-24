import unittest, sys
from os import path

from PyQt5.QtWidgets import QApplication

from unittest.mock import Mock, patch
from interface import InterfaceModel, ImagePresenter, InterfaceView

THIS_DIR = path.dirname( path.realpath( __file__ ) )
ASSET_DIR = path.join( THIS_DIR, 'assets' )
TEST_DIR = path.join( ASSET_DIR, 'test', 'interface' )

def get_asset_path( name, ext = '.png' ):
	return path.join( TEST_DIR, name + ext )


class TestRequestPackage( unittest.TestCase ):
	def test_contains_path( self ):
		pass


class TestReturnPackage( unittest.TestCase ):
	def test_no_error_file_path_valid( self ):
		pass

	def test_invalid_file_path_error( self ):
		pass

	def test_no_error_contains_image( self ):
		pass

	def test_invalid_image_error( self ):
		pass

	def test_no_error_containes_color_tree( self ):
		pass

	def test_invalid_color_tree_error( self ):
		pass


class TestInterfaceView( unittest.TestCase ):
	def setUp( self ):
		self.app = QApplication( sys.argv )
		self.view = InterfaceView()

	def test_ui( self ):
		pass

	def test_set_image_success_stores_path( self ):
		test_img_path = get_asset_path( 'test_set_image_success_stores_path' )

		self.view.set_image( test_img_path )
		self.assertEqual( self.view.current_image_path, test_img_path )

		# reset view
		self.view = InterfaceView()

	def test_set_invalid_image_fails( self ):
		with self.assertRaises( FileNotFoundError ):
			self.view.set_image( '' )


class TestImagePresenter( unittest.TestCase ):
	def test_init_registers_observer( self ):
		model = Mock()
		view = Mock()

		presenter = ImagePresenter( view, model )

		model.register_observer.assert_called_once_with( presenter )

	def test_load_images( self ):
		pass

	def test_request_passed_to_model( self ):
		pass


class TestInterfaceModel( unittest.TestCase ) :
	def test_register_observer( self ):
		model = InterfaceModel()
		observer = Mock()

		model.register_observer( observer )
		self.assertIn( observer, model.observers )


	def test_notify_observers( self ):
		model = InterfaceModel()
		observer1, observer2 = Mock(), Mock()

		model.register_observer( observer1 )
		model.register_observer( observer2 )

		model.notify_model_update()
		observer1.model_updated.assert_called_once()
		observer2.model_updated.assert_called_once()

	def test_request_triggers_update( self ):
		pass

	def test_requested_path_stored( self ):
		pass

	def test_valid_path_loads_image( self ):
		pass

	def test_invalid_path_returns_error( self ):
		pass

	def test_valid_image_produces_color_tree( self ):
		pass

	def test_color_fail_returns_error( self ):
		pass

	def test_return_package_sent( self ):
		pass

if __name__ == '__main__':
	unittest.main()
