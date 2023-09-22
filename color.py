import numpy as np
from PIL import Image
from collections import defaultdict


class ColorTree:
	def __init__( self, color_set ):
		self.rgb_list = list(color_set)
		self.nearest_neighbor_tree = self.group_colors()

	def group_colors( self ):
		# lower triangular matrix of distances
		pairwise_distsq = find_pairwise_distsq( self.rgb_list )

		# sort by distance
		nearest_neighbors = sorted( pairwise_distsq, key=pairwise_distsq.get )

		return agglomerate_tree_from_pairs( len(self.rgb_list), nearest_neighbors )
	
	def get_tree( self ):
		# use the nested tree of color indices
		# to make a nested tree of color values
		return populate_tree_with_values( self.nearest_neighbor_tree, self.rgb_list )


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
		
		# The parent group becomes itself paired with next closest group
		groups[ min_id ] = [ groups[ min_id ], groups[ max_id ] ]

		# rewrite all associated group numbers
		for i in range(len(group_numbers)):
			if group_numbers[i] == max_id:
				group_numbers[i] = min_id

		num_groups -= 1
	return groups[min_id]


def populate_tree_with_values( tree, value_array ):
	if tree is None:
		return None

	stack = [(tree, None, None)]
	root = None

	while stack:
		current_tree, parent, idx = stack.pop()
		
		if isinstance(current_tree, int):
			value = value_array[current_tree]
		elif isinstance(current_tree, list):
			value = [None] * len(current_tree)
			for i, subtree in reversed(list(enumerate(current_tree))):
				stack.append((subtree, value, i))
		else:
			raise ValueError("Invalid tree node type")

		if parent is not None:
			parent[idx] = value
		else:
			root = value

	return root


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
	colors = set([ tuple(rgba[:3]) for rgba in image_array_rasterized ])
	return colors


def convert_element_recursive(elem):
	if isinstance(elem, np.ndarray):
		return elem.tolist()
	if isinstance(elem, np.integer):
		return int(elem)
	if isinstance(elem, tuple):
		return tuple(convert_element_recursive(e) for e in elem)
	if isinstance(elem, list):
		return [convert_element_recursive(e) for e in elem]
	return elem


def compare_nested_lists(lst1, lst2):
	# Convert elements for special types recursively
	lst1 = convert_element_recursive(lst1)
	lst2 = convert_element_recursive(lst2)
		
	# Base case: Directly compare if both elements are not lists
	if not (isinstance(lst1, list) and isinstance(lst2, list)):
		return lst1 == lst2

	# Lists are of different lengths, they can't be equal
	if len(lst1) != len(lst2):
		return False
	
	# Partition by type for meaningful comparisons
	def partition_by_type(lst):
		partition = defaultdict(list)
		for elem in lst:
			partition[type(elem)].append(elem)
		return partition
	
	partition1 = partition_by_type(lst1)
	partition2 = partition_by_type(lst2)
	
	# Check if partitions have the same keys (i.e., types)
	if set(partition1.keys()) != set(partition2.keys()):
		return False
	
	# Sort each type partition and compare recursively
	for typ in partition1.keys():
		sorted_partition1 = sorted(partition1[typ], key=str)
		sorted_partition2 = sorted(partition2[typ], key=str)
		
		for a, b in zip(sorted_partition1, sorted_partition2):
			if not compare_nested_lists(a, b):
				return False

	return True
