from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTreeView, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex
import sys
from os import path

from color import *


class InterfaceView( QWidget ):
	def __init__( self ):
		super().__init__()
		self.initUI()


	def initUI( self ):
		# Widgets
		self.image_view = QLabel( self )
		self.image_view.setSizePolicy(
			QSizePolicy.Ignored,
			QSizePolicy.Ignored
		)
		self.tree_view = QTreeView( self )
		self.button = QPushButton( 'Load Image', self )

		# Layouts
		self.main_layout = QHBoxLayout()
		self.control_layout = QVBoxLayout()

		self.main_layout.addWidget( self.image_view, 1 )
		self.main_layout.addLayout( self.control_layout, 1 )
		self.control_layout.addWidget( self.tree_view, 1 )
		self.control_layout.addWidget( self.button, 1 )

		self.setLayout( self.main_layout )


	def set_image( self, image_path ):
		if not path.isfile( image_path ):
			raise Exception( "Path doesn't exist!" )
		self.current_image_path = image_path

		pixmap = QPixmap( image_path )
		self.image_view.setPixmap(
			pixmap.scaled(
				self.image_view.size(),
				Qt.KeepAspectRatio,
				Qt.SmoothTransformation
			)
		)
		return pixmap


	def resizeEvent( self, event ):
		if self.image_view.pixmap():
			self.set_image( self.current_image_path )


class ImagePresenter:
	def __init__( self, view, model ):
		self.view = view
		self.model = model
		self.model.register_observer( self )
		self.view.button.clicked.connect( self.load_image )


	def model_updated(self):
		# Update view based on model changes.
		self.set_tree_view( self.model.color_tree )


	def load_image(self):
		options = QFileDialog.Options()
		image_path, _ = QFileDialog.getOpenFileName(
			self.view,
			"QFileDialog.getOpenFileName()",
			"",
			"PNG Files (*.png);;All Files (*)",
			options=options )
		self.model.image = self.view.set_image( image_path )
		self.model.process_image( image_path )


	def set_tree_view( self, color_tree ):
		tree_view = self.view.tree


class InterfaceModel( QAbstractItemModel ):
	def __init__( self ):
		self.observers = []


	def process_image( self, path ):
		self.colors = get_colors( path )
		self.color_tree = ColorTree( self.colors )

		## Move the tree information over
		self.tree_model = TreeModel( self.color_tree )
		self.notify_observers()


if __name__ == "__main__":
	app = QApplication(sys.argv)

	model = InterfaceModel()
	view = InterfaceView()
	presenter = ImagePresenter(view, model)

	view.show()
	sys.exit(app.exec_())
