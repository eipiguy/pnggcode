from test_header import *
from octree import *

class TestOctree( unittest.TestCase ):

	def test_empty_tree( self ):
		octree = Octree( [] )
		self.assertEqual( octree.points, set() )


	def test_single_point( self ):
		octree = Octree( [(1, 1, 1)] )
		self.assertEqual( octree.points, {(1, 1, 1)} )


	def test_repeated_point( self ):
		octree = Octree( [ (1, 1, 1), (1, 1, 1) ] )
		self.assertEqual( octree.points, {(1, 1, 1)} )


	def test_nearby_points( self ):
		octree = Octree( [ (0, 0, 0), (1e-13, 1e-13, 1e-13) ] )
		self.assertEqual( octree.octants['000'].points, { (0, 0, 0) } )
		self.assertEqual( octree.octants['111'].points, { (1e-13, 1e-13, 1e-13) } )


	def test_octant_corner_points( self ):
		octree = Octree(
			[
				(0, 0, 0),
				(0, 0, 1),
				(0, 1, 0),
				(0, 1, 1),
				(1, 0, 0),
				(1, 0, 1),
				(1, 1, 0),
				(1, 1, 1)
			]
		)
		self.assertEqual( octree.octants['000'].points, { (0, 0, 0) } )
		self.assertEqual( octree.octants['001'].points, { (0, 0, 1) } )
		self.assertEqual( octree.octants['010'].points, { (0, 1, 0) } )
		self.assertEqual( octree.octants['011'].points, { (0, 1, 1) } )
		self.assertEqual( octree.octants['100'].points, { (1, 0, 0) } )
		self.assertEqual( octree.octants['101'].points, { (1, 0, 1) } )
		self.assertEqual( octree.octants['110'].points, { (1, 1, 0) } )
		self.assertEqual( octree.octants['111'].points, { (1, 1, 1) } )


	def test_octant_midpoint( self ):
		octree = Octree(
			[
				(0, 0, 0),
				(0, 0, 2),
				(0, 2, 0),
				(0, 2, 2),
				(2, 0, 0),
				(2, 0, 2),
				(2, 2, 0),
				(2, 2, 2),
				(1, 1, 1)
			]
		)
		self.assertEqual( octree.octants['000'].points, { (0, 0, 0) } )
		self.assertEqual( octree.octants['001'].points, { (0, 0, 2) } )
		self.assertEqual( octree.octants['010'].points, { (0, 2, 0) } )
		self.assertEqual( octree.octants['011'].points, { (0, 2, 2) } )
		self.assertEqual( octree.octants['100'].points, { (2, 0, 0) } )
		self.assertEqual( octree.octants['101'].points, { (2, 0, 2) } )
		self.assertEqual( octree.octants['110'].points, { (2, 2, 0) } )

		# border point always to far corner
		# this is determined by get_split_id
		self.assertEqual(
			octree.octants['111'].points,
			{(1, 1, 1), (2, 2, 2)}
		)
		
		# # the only reasonable alternative is
		# # to put border points in the near corner
		# self.assertEqual(
		# 	octree.octants['000'].points,
		# 	{(0, 0, 0), (1, 1, 1)}
		# )


	def test_octant_nesting( self ):
		octree = Octree(
			[
				(0, 0, 0),
				(0, 0, 3),
				(0, 3, 0),
				(0, 3, 3),
				(3, 0, 0),
				(3, 0, 3),
				(3, 3, 0),
				(3, 3, 3),

				(1, 1, 1),
				(1, 1, 2),
				(1, 2, 1),
				(1, 2, 2),
				(2, 1, 1),
				(2, 1, 2),
				(2, 2, 1),
				(2, 2, 2),
			]
		)
		self.assertEqual( octree.octants['000'].points, { (0, 0, 0), (1, 1, 1) } )
		self.assertEqual( octree.octants['001'].points, { (0, 0, 3), (1, 1, 2) } )
		self.assertEqual( octree.octants['010'].points, { (0, 3, 0), (1, 2, 1) } )
		self.assertEqual( octree.octants['011'].points, { (0, 3, 3), (1, 2, 2) } )
		self.assertEqual( octree.octants['100'].points, { (3, 0, 0), (2, 1, 1) } )
		self.assertEqual( octree.octants['101'].points, { (3, 0, 3), (2, 1, 2) } )
		self.assertEqual( octree.octants['110'].points, { (3, 3, 0), (2, 2, 1) } )
		self.assertEqual( octree.octants['111'].points, { (3, 3, 3), (2, 2, 2) } )


	def test_roll_call( self ):
		octree = Octree(
			[
				(0, 0, 0),
				(0, 0, 1),
				(0, 1, 0),
				(0, 1, 1),
				(1, 0, 0),
				(1, 0, 1),
				(1, 1, 0),
				(1, 1, 1)
			]
		)
		roll = octree.roll_call()
		self.assertEqual( roll['000'], {(0, 0, 0)} )
		self.assertEqual( roll['001'], {(0, 0, 1)} )
		self.assertEqual( roll['010'], {(0, 1, 0)} )
		self.assertEqual( roll['011'], {(0, 1, 1)} )
		self.assertEqual( roll['100'], {(1, 0, 0)} )
		self.assertEqual( roll['101'], {(1, 0, 1)} )
		self.assertEqual( roll['110'], {(1, 1, 0)} )
		self.assertEqual( roll['111'], {(1, 1, 1)} )


if __name__ == '__main__':
	unittest.main()