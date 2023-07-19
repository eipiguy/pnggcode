import numpy as np
from PIL import Image

class ColorTree:
	def __init__( self, rgb_color_list ):
		self.rgb_color_list = rgb_color_list
		self.binary_tree = self.map_connections()

	def map_connections( self ):
		pass

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