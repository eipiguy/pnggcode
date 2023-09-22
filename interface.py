from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTreeView, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

import sys
from os import path

from color import *


class InterfaceView( QWidget ):
	def __init__( self ):
		super().__init__()
		self.initUI()


	def initUI( self ):
		# Widgets
		self.label = QLabel( self )
		self.label.setSizePolicy(
			QSizePolicy.Ignored,
			QSizePolicy.Ignored
		)
		self.tree = QTreeView( self )
		self.button = QPushButton( 'Load Image', self )

		# Layouts
		self.main_layout = QHBoxLayout()
		self.control_layout = QVBoxLayout()

		self.main_layout.addWidget( self.label, 1 )
		self.main_layout.addLayout( self.control_layout, 1 )
		self.control_layout.addWidget( self.tree, 1 )
		self.control_layout.addWidget( self.button, 1 )

		self.setLayout( self.main_layout )


	def set_image( self, image_path ):
		if not path.isfile( image_path ):
			raise Exception( "Path doesn't exist!" )
		self.current_image_path = image_path

		pixmap = QPixmap( image_path )
		self.label.setPixmap(
			pixmap.scaled(
				self.label.size(),
				Qt.KeepAspectRatio,
				Qt.SmoothTransformation
			)
		)


	def resizeEvent( self, event ):
		if self.label.pixmap():
			self.set_image( self.current_image_path )


class ImagePresenter:
	def __init__( self, view, model ):
		self.view = view
		self.model = model
		self.model.register_observer( self )
		self.view.button.clicked.connect( self.load_image )


	def model_updated(self):
		# Update view based on model changes.
		pass


	def load_image(self):
		options = QFileDialog.Options()
		filePath, _ = QFileDialog.getOpenFileName(
			self.view,
			"QFileDialog.getOpenFileName()",
			"",
			"PNG Files (*.png);;All Files (*)",
			options=options )
		if filePath:
			self.view.set_image( filePath )
			self.colors = get_colors( filePath )
			self.color_tree = ColorTree( self.colors )
			print()


class InterfaceModel:
	def __init__( self ):
		self.observers = []


	def register_observer( self, observer ):
		self.observers.append(observer)


	def notify_observers( self ):
		for observer in self.observers:
			observer.model_updated()


if __name__ == "__main__":
	app = QApplication(sys.argv)

	model = InterfaceModel()
	view = InterfaceView()
	presenter = ImagePresenter(view, model)

	view.show()
	sys.exit(app.exec_())
