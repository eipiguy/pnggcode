import unittest
from octree import median_vals

class TestMedianVals( unittest.TestCase ):

	def test_single_point( self ):
		self.assertEqual(
			median_vals( [ (3, 4) ] ),
			[3, 4]
		)


	def test_two_points( self ):
		self.assertEqual(
			median_vals(
				[
					(1, 2),
					(3, 4)
				]
			),
			[2, 3]
		)


	def test_multiple_points_odd( self ):
		self.assertEqual(
			median_vals(
				[
					(1, 2),
					(3, 4),
					(5, 6)
				]
			),
			[3, 4]
		)


	def test_multiple_points_even( self ):
		self.assertEqual(
			median_vals(
				[
					(1, 2),
					(3, 4),
					(5, 6),
					(7, 8)
				]
			),
			[4, 5]
		)


	def test_non_integer_coordinates( self ):
		self.assertAlmostEqual( median_vals( [(1.1, 2.2), (3.3, 4.4)] )[0], 2.2, places = 10 )
		self.assertAlmostEqual( median_vals( [(1.1, 2.2), (3.3, 4.4)] )[1], 3.3, places = 10 )


	def test_high_dimensionality( self ):
		self.assertEqual(
			median_vals(
				[
					(1, 2, 3),
					(4, 5, 6),
					(7, 8, 9)
				]
			),
			[4, 5, 6]
		)


	def test_empty_set( self ):
		self.assertEqual(
			median_vals([]),
			None
		)


	def test_duplicate_points( self ):
		self.assertEqual(
			median_vals(
				[
					(1, 2),
					(1, 2),
					(3, 4)
				]
			),
			[1, 2]
		)


	def test_extreme_values_even( self ):
		self.assertAlmostEqual( median_vals( [(1e9, 1e-9), (1e-9, 1e9)] )[0], 0.5e9, places = 10 )
		self.assertAlmostEqual( median_vals( [(1e9, 1e-9), (1e-9, 1e9)] )[1], 0.5e9, places = 10 )


	def test_extreme_values_odd( self ):
		self.assertAlmostEqual( median_vals( [(1e9, 1e-9), (1e-9, 1e9), (1e9, 1e9)] )[0], 1e9, places = 10 )
		self.assertAlmostEqual( median_vals( [(1e9, 1e-9), (1e-9, 1e9), (1e9, 1e9)] )[1], 1e9, places = 10 )


	def test_non_uniform_distribution( self ):
		self.assertEqual(
			median_vals(
				[(1, 1000), (2, 1000), (3, 1000)]
			),
			[2, 1000]
		)


	def test_overflow( self ):
		self.assertAlmostEqual( median_vals( [(1e308, 1e308), (-1e308, -1e308), (0, 0)] )[0], 0, places = 10 )
		self.assertAlmostEqual( median_vals( [(1e308, 1e308), (-1e308, -1e308), (0, 0)] )[1], 0, places = 10 )


if __name__ == "__main__":
	unittest.main()
