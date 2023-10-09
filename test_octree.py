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


	def test_cube_directions( self ):
		directions_ids = cube_directions()
		# deleted 3x3x3 neighborhood has
		# 27 - self = 26 members
		self.assertEqual( len(directions_ids), 26 )


# 	def test_id_direction_single_lvl( self ):
# 		source_id = '010'
# 		dest_id = '101'
# 		direction = id_direction( source_id, dest_id )
# 		self.assertEqual( direction, '1,-1,1' )
# 
# 
# 	def test_id_direction_multiple_lvls( self ):
# 		source_id = '000 010 111'
# 		dest_id = '111 101 000'
# 		direction = id_direction( source_id, dest_id )
# 		self.assertEqual( direction, '1,1,1 1,-1,1 -1,-1,-1' )


	def test_follow_direction_positive( self ):
		source_id = '001 011 111'
		direction = '1,1,1'
		dest_id, remaining_dir = resolve_direction( source_id, direction )
		self.assertEqual( dest_id, '010 100 000' )
		self.assertEqual( remaining_dir, '0,0,1' )


	def test_follow_direction_negative( self ):
		source_id = '110 100 000'
		direction = '-1,-1,-1'
		dest_id, remaining_dir = resolve_direction( source_id, direction )
		self.assertEqual( dest_id, '101 011 111' )
		self.assertEqual( remaining_dir, '0,0,-1' )


	def test_siblings_parent( self ):
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
		poll_id = '111' # = {( 1, 1, 1)}
		siblings = octree.sibling_coords( poll_id )

		self.assertIn( '000', siblings )
		self.assertIn( '001', siblings )
		self.assertIn( '010', siblings )
		self.assertIn( '011', siblings )
		self.assertIn( '100', siblings )
		self.assertIn( '101', siblings )
		self.assertIn( '110', siblings )

		self.assertNotIn( '111', siblings )
		self.assertEqual( len(siblings), 7 )


	def test_siblings_nested( self ):
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
		poll_id = '000 111' # = {( 1, 1, 1)}
		siblings = octree.sibling_coords( poll_id )
		self.assertIn( '000 000', siblings )
		self.assertNotIn( '000 111', siblings )
		self.assertEqual( len(siblings), 1 )


	def test_neighbor_ids( self ):
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
		

		# Without being on a boundary,
		# there should be a 3x3x3 cube
		# of neighbor cells minus the center,
		# thus (9*3)-1 = 26 neighbors

		# 000 ->
		# at initial levels,
		# you are always on a boundary
		# so children just return siblings

		# for deeper levels
		poll_id = '000 111' # = {( 1, 1, 1)}
		neighbor_ids = octree.neighbor_ids( poll_id )
		self.assertEqual( len(neighbor_ids), 26 )
		self.assertNotIn( '000 111', neighbor_ids )


	def test_neighbors( self ):
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
		

		# Without being on a boundary,
		# there should be a 3x3x3 cube
		# of neighbor cells minus the center,
		# thus (9*3)-1 = 26 neighbors

		# 000 ->
		# at initial levels,
		# you are always on a boundary
		# so children just return siblings

		# for deeper levels
		poll_id = '000 111' # = {( 1, 1, 1)}
		neighbors = octree.neighbors( poll_id )
		self.assertEqual( len(neighbors), 8 )


if __name__ == '__main__':
	unittest.main()
