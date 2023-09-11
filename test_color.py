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
		colors = get_colors( image )
		self.assertEqual( len( colors ), 1 )

	def test_get_colors_four_color_image( self ):
		image = self.get_image( 'test_get_colors_four_color_image' )
		colors = get_colors( image )
		self.assertEqual( len( colors ), 4 )

class TestNestedListCompare(unittest.TestCase):
	def test_identical_lists(self):
		self.assertTrue(compare_nested_lists(
			[[1, 2], [3, 4]],
			[[1, 2], [3, 4]]
		))

	def test_order_agnostic(self):
		self.assertTrue(compare_nested_lists(
			[[1, 2], [3, 4]],
			[[4, 3], [1, 2]]
		))

	def test_different_lists(self):
		self.assertFalse(compare_nested_lists(
			[[1, 2], [3, 4]],
			[[1, 2], [3, 5]]
		))

	def test_different_lengths(self):
		self.assertFalse(compare_nested_lists(
			[[1, 2], [3, 4]],
			[[1, 2]]
		))

	def test_different_depths(self):
		self.assertFalse(compare_nested_lists(
			[[1, 2], [3, 4]],
			[[1, 2], [[3, 4]]]
		))

	def test_empty_lists(self):
		self.assertTrue(compare_nested_lists(
			[],
			[]
		))
	
	def test_single_element(self):
		self.assertTrue(compare_nested_lists(
			[1],
			[1]
		))
	
	def test_none_elements(self):
		self.assertTrue(compare_nested_lists(
			[None],
			[None]
		))
		self.assertFalse(compare_nested_lists(
			[None],
			[1]
		))

	def test_mixed_types_order_agnostic(self):
		self.assertTrue(compare_nested_lists(
			[1, "1", None],
			[None, 1, "1"]
		))
	
	def test_repeated_elements(self):
		self.assertTrue(compare_nested_lists([1, 1, 1], [1, 1, 1]))
		self.assertFalse(compare_nested_lists([1, 1, 1], [1, 1]))
	
	def test_nested_repeated_elements(self):
		self.assertTrue(compare_nested_lists(
			[[1, 1], [1, 1]],
			[[1, 1], [1, 1]]
		))
		self.assertFalse(compare_nested_lists(
			[[1, 1], [1, 1]],
			[[1, 1], [1]]
		))
	
	def test_deeply_nested_lists(self):
		self.assertTrue(compare_nested_lists(
			[[[1]]],
			[[[1]]]
		))
		self.assertFalse(compare_nested_lists(
			[[[1]]],
			[[[2]]]
		))
	
	def test_mismatched_depth(self):
		self.assertFalse(compare_nested_lists(
			[1, [1]],
			[1, 1]
		))

	def test_different_int_formats(self):
		self.assertTrue(compare_nested_lists(
			[[1, 2], [3, 4]],
			[[np.uint8(1), np.uint8(2)], [np.uint8(3), np.uint8(4)]]
		))

	def test_compare_simple_np_array(self):
		self.assertTrue(compare_nested_lists(
			np.array([1, 2]),
			[1, 2]
		))

	def test_compare_simple_np_array_mismatch(self):
		self.assertFalse(compare_nested_lists(
			np.array([1, 2]),
			[1, 3]
		))

	def test_compare_list_of_np_arrays(self):
		self.assertTrue(compare_nested_lists(
			[np.array([1, 2]), np.array([3, 4])],
			[[1, 2], [3, 4]]
		))

	def test_compare_list_of_np_arrays_order_agnostic(self):
		self.assertTrue(compare_nested_lists(
			[np.array([1, 2]), np.array([3, 4])],
			[[3, 4], [2, 1]]
		))

	def test_compare_2D_np_array(self):
		self.assertTrue(compare_nested_lists(
			np.array([[1, 2], [3, 4]]),
			[[1, 2], [3, 4]]
		))

	def test_compare_mixed_list_and_np_array(self):
		self.assertTrue(compare_nested_lists(
			[1, np.array([2, 3])],
			[1, [2, 3]]
		))

	def test_identical_tuple_lists(self):
		self.assertTrue(compare_nested_lists(
			[(1, 2), (3, 4)],
			[(1, 2), (3, 4)]
		))
	
	def test_different_tuple_int_formats(self):
		self.assertTrue(compare_nested_lists(
			[(1, 2), (3, 4)],
			[(np.int8(1), np.int8(2)), (np.int8(3), np.int8(4))]
		))

	def test_nested_tuple_mismatch(self):
		self.assertFalse(compare_nested_lists(
			[[(1, 2)], [(3, 4)]],
			[[(1, 2)], [(3, 5)]]
		))

	def test_nested_tuple_lists(self):
		self.assertTrue(compare_nested_lists(
			[[(1, 2)], [(3, 4)]],
			[[(1, 2)], [(3, 4)]]
		))
		self.assertFalse(compare_nested_lists(
			[[(1, 2)], [(3, 4)]],
			[[(1, 2)], [(4, 3)]]
		))

class TestPopulateTree(unittest.TestCase):
	def test_basic_functionality(self):
		tree = [[0, 1], 2]
		value_array = ['a', 'b', 'c']
		self.assertEqual(
			populate_tree_with_values(tree, value_array),
			[['a', 'b'], 'c']
		)

	def test_empty_tree(self):
		tree = None
		value_array = ['a', 'b', 'c']
		self.assertEqual(
			populate_tree_with_values(tree, value_array),
			None
		)

	def test_single_element_tree(self):
		tree = 0
		value_array = ['a']
		self.assertEqual(
			populate_tree_with_values(tree, value_array),
			'a'
		)

	def test_non_integer_tree(self):
		tree = ["invalid_node"]
		value_array = ['a', 'b', 'c']
		with self.assertRaises(ValueError):
			populate_tree_with_values(tree, value_array)

	def test_deeper_nesting(self):
		tree = [[[0, 1], 2], [3, 4]]
		value_array = ['a', 'b', 'c', 'd', 'e']
		self.assertEqual(
			populate_tree_with_values(tree, value_array),
			[[['a', 'b'], 'c'], ['d', 'e']]
		)

	def test_irregular_nesting(self):
		tree = [[0, [1, 2]], [3, [4, [5, 6]]]]
		value_array = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
		self.assertEqual(
			populate_tree_with_values(tree, value_array),
			[['a', ['b', 'c']], ['d', ['e', ['f', 'g']]]]
		)

class TestAgglomerateTree( unittest.TestCase ):
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
		test_colors = get_colors( self.get_image( 'test_map_color_connections' ) )

		# create binary tree of nearest color groups
		color_tree = ColorTree( test_colors )

		test_color_tree = color_tree.get_tree()
		# check against baseline
		self.assertTrue( compare_nested_lists( test_color_tree, baseline_color_tree ) )

if __name__ == "__main__":
	unittest.main( )
