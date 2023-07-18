import numpy as np
from PIL import Image

class ColorTree:
	def __init__( self, rgb_color_list ):
		self.rgb_color_list = rgb_color_list

	def map_connections( self ):
		pass

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
