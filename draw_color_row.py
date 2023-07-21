
from color import *
from png_draw import *

colors = []
blue_75 = ( 0, 0, 75 )
blue_100 = ( 0, 0, 100 )

colors.append( blue_75 )
colors.append( blue_100 )
colors.append( grey_triple_255( 0 ) )
colors.append( grey_triple_255( 25 ) )
colors.append( grey_triple_255( 250 ) )
colors.append( grey_triple_255( 255 ) )

color_row = NImage( 1, len( colors ))
color_row.draw_rgb_array( [ colors ] )
color_row.write_png( 'color_row.png' )