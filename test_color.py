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

	def test_get_colors_single_color_image( self ):
		image = self.get_image( 'test_get_colors_single_color_image' )
		colors, color_counts = get_colors( image )
		self.assertEqual( len( colors ), 1 )

	def test_get_colors_four_color_image( self ):
		image = self.get_image( 'test_get_colors_four_color_image' )
		colors, color_counts = get_colors( image )
		self.assertEqual( len( colors ), 4 )

class TestNestedListCompare( unittest.TestCase ):
	def test_identical_lists( self ):
		lst1 = [
			[ ( 1, 2 ), ( 3, 4 ) ],
			[ ( 5, 6 ), ( 7, 8 ) ] ]
		lst2 = [
			[ ( 1, 2 ), ( 3, 4 ) ],
			[ ( 5, 6 ), ( 7, 8 ) ] ]
		self.assertTrue( compare_nested_lists( lst1, lst2 ))

	def test_different_lists( self ):
		lst1 = [
			[ ( 1, 2 ), ( 3, 4 ) ],
			[ ( 5, 6 ), ( 7, 8 ) ] ]
		lst2 = [
			[ ( 1, 2 ), ( 3, 5 ) ],
			[ ( 5, 6 ), ( 7, 8 ) ] ]
		self.assertFalse( compare_nested_lists( lst1, lst2 ))

	def test_different_lengths( self ):
		lst1 = [
			[ ( 1, 2 ), ( 3, 4 ) ],
			[ ( 5, 6 ), ( 7, 8 ) ] ]
		lst2 = [
			[ ( 1, 2 ), ( 3, 4 ) ] ]
		self.assertFalse( compare_nested_lists( lst1, lst2 ))

	def test_different_depths( self ):
		lst1 = [
			[ ( 1, 2 ), ( 3, 4 ) ],
			[ ( 5, 6 ), ( 7, 8 ) ] ]
		lst2 = [
			[ ( 1, 2 ), [ ( 3, 4 ) ], ( 5, 6 ) ],
			[ ( 7, 8 ) ] ]
		self.assertFalse( compare_nested_lists( lst1, lst2 ))

class TestColorTree( unittest.TestCase ):
	def setUp( self ):
		this_dir = path.dirname( path.realpath( __file__ ) )
		self.test_dir = path.join( this_dir, 'assets', 'test' )

	def get_image( self, file_name, file_extension = 'png' ):
		return path.join( self.test_dir, file_name + '.' + file_extension )

	def test_basic_functionality(self):
		self.assertEqual(
			agglomerate_tree_from_pairs(3, [(0, 1), (1, 2)]),
			[[0, 1], 2]
		)

	def test_empty_input_list(self):
		self.assertEqual(
			agglomerate_tree_from_pairs(3, []),
			0
		)

	def test_non_unique_nearest_neighbors(self):
		self.assertEqual(
			agglomerate_tree_from_pairs(3, [(0, 1), (0, 1), (1, 2)]),
			[[0, 1], 2]
		)

	def test_single_element(self):
		self.assertEqual(
			agglomerate_tree_from_pairs(1, []),
			0
		)

	def test_map_color_connections( self ):

		blue_75 = ( 0, 0, 75 )
		blue_100 = ( 0, 0, 100 )
		baseline_color_tree = [
			[
				[
					grey_triple_255( 0 ),
					grey_triple_255( 25 )
				],
				[
					blue_75,
					blue_100
				]
			],
			[
				grey_triple_255( 250 ),
				grey_triple_255( 255 )
			]
		]

		# input a collection of unique colors
		colors = []
		colors.append( blue_75 )
		colors.append( blue_100 )
		colors.append( grey_triple_255( 0 ) )
		colors.append( grey_triple_255( 25 ) )
		colors.append( grey_triple_255( 250 ) )
		colors.append( grey_triple_255( 255 ) )
		test_colors, test_color_counts = get_colors( self.get_image( 'test_map_color_connections' ) )

		# create binary tree of nearest color groups
		test_color_tree = ColorTree( test_colors )

		# check against baseline
		self.assertTrue( compare_nested_lists( test_color_tree.get_tree(), baseline_color_tree ) )

if __name__ == "__main__":
	unittest.main( )