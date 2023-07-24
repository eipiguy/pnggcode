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

		print(nearest_neighbors)

		# build nearest neighbor binary tree
		num_final_colors = 16
		group_ids = get_nearest_neighbor_groups( len( self.rgb_list ), nearest_neighbors, num_final_colors )
		return group_ids

def get_nearest_neighbor_groups( num_elements, sorted_pair_list, desired_groups ):
	num_groups = num_elements
	group_numbers = [ list( range( num_elements ) ) ]
	unlinked_colors = [ True ]

	for pair in sorted_pair_list:
		if num_groups <= desired_groups:
			break
		cur_groups = group_numbers[-1]
		if len( set( cur_groups ) ) <= 1:
			break
		if cur_groups[ pair[0] ] == cur_groups[ pair[1] ]:
			continue
		new_group_numbers = [ cur_groups[ pair[0] ] if group == cur_groups[ pair[1] ] else group for group in cur_groups ]
		group_numbers.append( new_group_numbers )
		num_groups -= 1
		print( new_group_numbers )
	return group_numbers[-1]

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