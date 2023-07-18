import unittest
from os import path

from color import *

class TestGetColors( unittest.TestCase ):

	def setUp( self ):
		this_dir = path.dirname( path.realpath( __file__ ) )
		self.test_dir = path.join( this_dir, 'assets', 'test' )

	def get_image( self, file_name, file_extension = 'png' ):
		return path.join( self.test_dir, file_name + '.' + file_extension )

	def test_asset_dir_exists( self ):
		self.assertTrue( path.exists( self.test_dir ) )

	def test_get_colors_empty_image( self ):
		image = self.get_image( 'empty_temp' )
		colors, color_counts = get_colors( image )
		self.assertEqual( len( colors ), 0 )

	def test_get_colors_single_color_image( self ):
		image = self.get_image( 'single_color' )
		colors, color_counts = get_colors( image )
		self.assertEqual( len( colors ), 1 )
		self.assertEqual( colors[0], [255, 0, 0] )

	def test_get_colors_multi_color_image( self ):
		image = self.get_image( 'multi_color' )
		colors, color_counts = get_colors( image )
		self.assertEqual( len( colors ), 3 )
		self.assertEqual( colors[0], [ 255, 0, 0 ] )
		self.assertEqual( colors[1], [ 0, 255, 0 ] )
		self.assertEqual( colors[2], [ 0, 0, 255 ] )

if __name__ == "__main__":
	unittest.main( )