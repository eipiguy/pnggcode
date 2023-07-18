import unittest, os
from os import path

from png_draw import *

class TestPngDraw( unittest.TestCase ):

	def setUp( self ):
		this_dir = path.dirname( path.realpath( __file__ ) )
		self.test_dir = path.join( this_dir, 'assets', 'test' )
		self.test_img_path = path.join( self.test_dir, 'test.png' )

	def baseline( self, file_name, file_extension = 'png' ):
		return path.join( self.test_dir, file_name + '.' + file_extension )

	def test_asset_dir_exists( self ):
		self.assertTrue( path.exists( self.test_dir ) )

	def test_draw_single_pixel_png( self ):
		test_img = NImage( 1, 1 )
		test_img.write_png( self.test_img_path )
		
		self.assertTrue( compare_pngs( self.test_img_path, self.baseline( 'test_draw_single_pixel_png' ) ) )

		os.remove( self.test_img_path )
	
	def test_draw_four_color_png( self ):
		test_img = NImage( 2, 2 )

		color_black = ( 0, 0, 0 )
		color_red = ( 255, 0, 0 )
		top_row = [ color_black, color_red ]

		color_green = ( 0, 255, 0 )
		color_blue = ( 0, 0, 255 )
		bottom_row = [ color_green, color_blue ]

		color_llist = [ top_row, bottom_row ]

		test_img.draw_rgb_array( color_llist )
		test_img.write_png( self.test_img_path )
		
		self.assertTrue( compare_pngs( self.test_img_path, self.baseline( 'test_draw_four_color_png' ) ) )

		os.remove( self.test_img_path )

if __name__ == '__main__':
	unittest.main()
