from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex
from PyQt5.QtGui import QBrush, QColor
from PIL import Image

from octree import Octree, component_vals


class TreeNode:
	def __init__(self, data, parent=None):
		self.parent = parent
		self.children = []
		self.is_collapsed = True
		self.bind_octree( data )

	def bind_octree( self, octree ):
		self.data = octree

		# first set the current node's data
		self.average_color = self.color_average()

		if hasattr( octree, 'octants' ):
			# then process all the children nodes
			for corner_id in octree.octants:
				corner = octree.octants[corner_id]
				child_node = TreeNode( corner, self )
				self.children.append( child_node )

	def color_average( self ):
		if len(self.data.points) == 1:
			self.average_color = list(self.data.points)[0]
			return self.average_color

		vals = component_vals( self.data.points )
		avg_vals = [ int(sum( comp_vals ) / len(comp_vals)) for comp_vals in vals ]
		self.average_color = tuple(avg_vals)
		return self.average_color

	def do_recursively( self, operation, inputs ):
		octree = self.data

		# if there are children
		if hasattr( octree, 'octants' ):

			# then process all the children nodes
			for corner_id in octree.octants:
				corner = octree.octants[corner_id]

		# if there are no children
		else:
		
			pass


	def make_all_masks( self, pil_p_image ):
		octree = self.data

		# make an empty mask the size of the image
		width, height = pil_p_image.size
		pil_rgb_image = pil_p_image.convert( 'RGB' )
		self.mask = Image.new( "RGBA", ( width, height ), ( 0, 0, 0, 0 ) )
		self.undo_mask = Image.new( "RGBA", ( width, height ), ( 0, 0, 0, 0 ) )
		self.locations = []

		# if there are children
		if len( self.children ) > 0:

			# process all the children nodes
			for child in self.children:

				# set the masks for each child
				child.make_all_masks( pil_rgb_image )

				# and conglomerate onto the parent copy
				if len( child.locations ) > 0:
					self.locations.extend( child.locations )
					for location in child.locations:
						self.mask.putpixel( location, self.average_color )
						if child.is_collapsed:
							self.undo_mask.putpixel( location, child.average_color )
						else:
							self.undo_mask.putpixel( location, child.average_color )

			# remove repeated locations
			self.locations = set( self.locations )

		# if there are no children, we have to make the mask manually
		else:
			for y in range(height):
				for x in range(width):
					location = ( x, y )
					pixel = pil_rgb_image.getpixel( location )
					if pixel in octree.points:
						self.locations.append( location )
						self.mask.putpixel( location, self.average_color )

		# children or no children,
		# the undo mask is set after the color locations have been confirmed
		for location in self.locations:

			# if there are children
			if len( self.children ) > 0:

				# process all the children nodes
				for child in self.children:

					# For the undo mask,
					# we pick the state of the child
					# which has that location
					# (children are a partition)
					if location in child.locations:
						pixel = child.undo_mask.getpixel( location )
						break
			# if we don't have children,
			# we use the original image data
			else:
				pixel = pil_p_image.getpixel( location )

			# either way, we add the pixel to the mask
			self.undo_mask.putpixel( location, pixel )


class TreeModel( QAbstractItemModel ):
	def __init__( self, pil_p_image ):
		super( TreeModel, self ).__init__()
		color_set = pil_p_image.palette.colors
		self.color_octree = Octree( color_set )
		self.root = TreeNode( self.color_octree )
		self.root.make_all_masks( pil_p_image )


	def index( self, row, column, parent = QModelIndex() ):
		# return index to root node if parent not valid
		if not parent.isValid():
			return self.createIndex( row, column, self.root.children[row] )

		# otherwise return the specified index of the child
		parent_node = parent.internalPointer()
		return self.createIndex( row, column, parent_node.children[row] )


	def parent( self, index ):
		if not index.isValid():
			# return the default (root?) index
			# if the input doesn't exist
			return QModelIndex()

		# internalPointer is a QAbstractItemModel function
		node = index.internalPointer()
		parent_node = node.parent

		# return the default (root?) index
		# if the parent is the root node
		if parent_node is self.root:
			return QModelIndex()

		# otherwise we need to make an index
		# with information from the grandparent
		grandparent_node = parent_node.parent
		if grandparent_node:

			# find position of parent in list of aunts/uncles
			row = grandparent_node.children.index(parent_node)
			return self.createIndex(row, 0, parent_node)

		return QModelIndex()


	def rowCount( self, parent = QModelIndex() ):
		if not parent.isValid():
			return len(self.root.children)

		# number of branches at current node (siblings)
		parent_node = parent.internalPointer()
		return len(parent_node.children)


	def columnCount( self, parent = QModelIndex() ):
		# we are not using matrix links at each node point,
		# just a one-dimensional list of branches
		return 1


	def data( self, index, role=Qt.DisplayRole ):
		if not index.isValid():
			return None

		if role == Qt.DisplayRole:
			tree_node = index.internalPointer()
			return str( tree_node.average_color )

		if role == Qt.BackgroundRole:
			tree_node = index.internalPointer()
			return QBrush( QColor( *tree_node.average_color ) )

		return None
