from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTreeView, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex
import sys
from os import path
from PIL import Image

from color_tree import TreeModel


class InterfaceView( QWidget ):
	def __init__( self ):
		super().__init__()
		self.initUI()
		self.pixmap = QPixmap()


	def initUI( self ):
		# Image Panel
		self.image_view = QLabel( self )
		self.image_view.setSizePolicy(
			QSizePolicy.Ignored,
			QSizePolicy.Ignored
		)

		# Control Panel
		self.tree_view = QTreeView( self )
		self.button = QPushButton( 'Load Image', self )

		# Organizing Layouts
		self.main_layout = QHBoxLayout()
		self.control_layout = QVBoxLayout()

		self.main_layout.addWidget( self.image_view, 1 )
		self.main_layout.addLayout( self.control_layout, 1 )
		self.control_layout.addWidget( self.tree_view, 1 )
		self.control_layout.addWidget( self.button, 1 )

		self.setLayout( self.main_layout )


	def set_pixmap( self, pixmap ):
		self.pixmap = pixmap
		self.show_pixmap()


	def show_pixmap( self ):
		self.image_view.setPixmap(
			self.pixmap.scaled(
				self.image_view.size(),
				Qt.KeepAspectRatio,
				Qt.FastTransformation
			)
		)


	def resizeEvent( self, event ):
		self.show_pixmap()


class ImagePresenter:
	def __init__( self, view, model ):
		self.view = view
		self.model = model
		self.model.register_observer( self )
		self.view.button.clicked.connect( self.load_image )


	def node_expanded( self, qt_index ):
		self.model.node_expanded( qt_index )


	def node_collapsed( self, qt_index ):
		self.model.node_collapsed( qt_index )


	def model_updated( self ):
		# Update view based on model changes.
		self.view.tree_view.setModel( self.model.tree_model )
		self.view.tree_view.expanded.connect( self.node_expanded )
		self.view.tree_view.collapsed.connect( self.node_collapsed )


	def display_updated( self, display ):
		display_pixmap = pil_to_qpixmap( display )
		self.view.set_pixmap( display_pixmap )


	def load_image( self ):
		options = QFileDialog.Options()
		image_path, _ = QFileDialog.getOpenFileName(
			self.view,
			"QFileDialog.getOpenFileName()",
			"",
			"PNG Files (*.png);;All Files (*)",
			options = options )
		self.view.set_pixmap( QPixmap( image_path ) )
		self.model.process_image( image_path )


def pil_to_qpixmap(pil_image):
	# Convert PIL image to QImage
	pil_image = pil_image.convert("RGBA")
	qimage = QImage(pil_image.tobytes('raw', 'RGBA'), pil_image.size[0], pil_image.size[1], QImage.Format_RGBA8888)
	
	# Convert QImage to QPixmap
	qpixmap = QPixmap.fromImage(qimage)
	return qpixmap


class InterfaceModel( QAbstractItemModel ):
	def __init__( self ):
		super( QAbstractItemModel, self ).__init__()
		self.observers = []


	def register_observer( self, new_observer ):
		self.observers.append( new_observer )


	def notify_model_update( self ):
		for observer in self.observers:
			observer.model_updated()


	def notify_display_update( self, display ):
		for observer in self.observers:
			observer.display_updated( display )


	def process_image( self, path ):
		image = Image.open( path ).convert( 'RGB' )
		self.image = image
		self.display = image.convert( 'RGBA' )

		# Get color palette and make tree
		palette_image = image.convert('P', palette=Image.ADAPTIVE)
		self.colors = palette_image.palette.colors

		# The tree is a way of indexing the palette
		self.tree_model = TreeModel( palette_image )
		self.notify_model_update()


	def get_color_locations( self, colors ):
		locations = []
		width, height = self.image.size
		for y in range(height):
			for x in range(width):
				xy_pixel = self.image.getpixel( ( x, y ) )
				if xy_pixel in colors:
					# save the location, and the original color
					# (for undo mask)
					locations.append( ( x, y ) )
		return locations


	def make_mask( self, locations, color = ( 255, 255, 255, 255) ):
		# make an empty mask the size of the image
		width, height = self.image.size
		mask = Image.new( "RGBA", ( width, height ), ( 0, 0, 0, 0 ) )
		undo_mask = Image.new( "RGBA", ( width, height ), ( 0, 0, 0, 0 ) )
		for y in range(height):
			for x in range(width):
				if ( x, y ) in locations:
					mask.putpixel( ( x, y ), color )
					undo_mask.putpixel( ( x, y ), self.display.getpixel( ( x, y ) ) )
		return mask, undo_mask


	def node_collapsed( self, qt_index ):
		node = qt_index.internalPointer()

		# mask replaces group colors with average
		# for the currently displayed image
		self.display = Image.alpha_composite( self.display, node.mask )
		node.is_collapsed = True

		# tell observers
		self.notify_display_update( self.display )


	def node_expanded( self, qt_index ):
		node = qt_index.internalPointer()

		# undo mask replaces a average color with
		# average or group, based on children
		self.display = Image.alpha_composite( self.display, node.undo_mask )
		node.is_collapsed = False

		self.notify_display_update( self.display )


if __name__ == "__main__":
	app = QApplication(sys.argv)

	model = InterfaceModel()
	view = InterfaceView()
	presenter = ImagePresenter(view, model)

	view.show()
	sys.exit(app.exec_())
