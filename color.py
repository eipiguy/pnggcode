import numpy as np
from PIL import Image

class ColorGroup:
	def __init__( self, rgb_list ):
		pass

class ColorTree:
	def __init__( self, rgb_list ):
		self.rgb_list = rgb_list
		color_groups = self.group_colors()

	def group_colors( self ):
		# lower triangular matrix of distances
		pairwise_distsq = find_pairwise_distsq( self.rgb_list )

		# sort by distance
		nearest_neighbors = sorted( pairwise_distsq, key=pairwise_distsq.get )

		self.nearest_neighbor_tree = agglomerate_tree_from_pairs( len(self.rgb_list), nearest_neighbors )
	
	def get_tree():
		# use the nested tree of color indices
		# to make a nested tree of color values
		pass

def agglomerate_tree_from_pairs( num_elements, sorted_neighbor_pairs ):
	if num_elements == 0:
		return None
	if num_elements == 1:
		return 0

	group_numbers = list( range( num_elements ) )
	groups = list( range( num_elements ) )
	num_groups = num_elements
	min_id = 0

	# all possible pairs in order of distance
	for pair in sorted_neighbor_pairs:
		
		# need to stop once we have a single group
		if num_groups < 1:
			break

		pair_group_numbers = [ group_numbers[ pair[0] ], group_numbers[ pair[1] ] ]
		min_id = min( pair_group_numbers )
		max_id = max( pair_group_numbers )
		if min_id == max_id:
			continue

		# always use the lower id as the parent for consistency
		#parent_id = pair[0] if pair_group_numbers[0] <= pair_group_numbers[1] else pair[1]
		
		# The parent group becomes itself paired with next closest group
		groups[ min_id ] = [ groups[ min_id ], groups[ max_id ] ]

		# rewrite all associated group numbers
		for i in range(len(group_numbers)):
			if group_numbers[i] == max_id:
				group_numbers[i] = min_id

		num_groups -= 1
	return groups[min_id]

def min_distsq( nested_left, nested_right, dist_dict ):
	min = np.inf
	for l_item in nested_left:
		if isinstance( l_item, list ):
			dist = min_distsq( l_item, nested_right )
			if dist < min:
				min = dist
		else:
			for r_item in nested_right:
				if isinstance( r_item, list ):
					dist = min_distsq( l_item, r_item )
				else:
					dist = dist_dict[(l_item,r_item)]
				if dist < min:
					min = dist
	return min

def find_pairwise_distsq( rgb_list ):
	pairwise_dict = {}

	# pairwise distances
	for i,first in enumerate( rgb_list ):
		for j,compare in enumerate( rgb_list[i+1:] ):
			pairwise_dict[(i,i+j+1)] = distsq( first, compare )

	return pairwise_dict

def distsq( tuple_l, tuple_r ):
	return sum( [ ( max((lhs, tuple_r[i]) - min(lhs, tuple_r[i]) ))**2 for i, lhs in enumerate( tuple_l ) ] )

def grey_triple_255( val ):
	return ( val, val, val )

def get_colors( image_path ):
	image = Image.open( image_path )
	image_array = np.array( image )

	# reshape to new size: size_x by size_y
	# -1 means adapt to fit
	image_array_rasterized = image_array.reshape( -1, image_array.shape[2] )

	# take RGBa colors and remove the alpha
	rgb_array = [ rgba[:3] for rgba in image_array_rasterized ]

	colors, color_counts = np.unique( rgb_array, return_counts = True, axis = 0 )
	return colors, color_counts

def compare_nested_lists( l_list, r_list ):
	if not l_list or not r_list:
		return False
	if len( l_list ) != len( r_list ):
		return False
	for i in range( len( l_list ) ):
		if type( l_list[i] ) != type( r_list[i] ):
			return False
		if isinstance( l_list[i], list ):
			if not compare_nested_lists( l_list[i],  r_list[i] ):
				return False
		elif l_list[i] != r_list[i]:
			return False
	return True