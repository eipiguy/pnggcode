import numpy as np
from PIL import Image

class NImage:
	def __init__( self, width, height, fill = ( 0, 0, 0, 0 ) ):
		self.pil_image = Image.new( 'RGBA', ( width, height ), fill )

	def write_png( self, file_path ):
		self.pil_image.save( file_path )

	def draw_rgb_array( self, rgb_array ):
		np_array = np.uint8( rgb_array )
		#np_array_transpose = np_array.transpose(1,2,0)
		self.pil_image = Image.fromarray( np_array, 'RGB' )

def compare_pngs( left_png_path, right_png_path ):
	left_png = Image.open(left_png_path)
	right_png = Image.open(right_png_path)

	# Check if images have the same size
	if left_png.size != right_png.size:
		return False

	# Compare pixels
	left_px = left_png.load()
	right_px = right_png.load()

	for x in range( left_png.width ):
		for y in range( left_png.height ):
			if left_px[ x, y ] != right_px[ x, y ]:
				return False

	return True
