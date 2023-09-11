from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTreeView, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

import sys

from color import *


class InterfaceView( QWidget ):
	def __init__( self ):
		super().__init__()
		self.initUI()

	def initUI( self ):
		# Layouts and widgets
		self.layout = QVBoxLayout()
		self.label = QLabel(self)
		self.tree = QTreeView(self)
		self.button = QPushButton( 'Load Image', self )
		

		self.layout.addWidget( self.label )
		self.layout.addWidget( self.tree )
		self.layout.addWidget( self.button )

		self.setLayout(self.layout)
		
	def set_image( self, image_path ):
		pixmap = QPixmap( image_path )
		self.label.setPixmap( pixmap )


class ImagePresenter:
	def __init__(self, view, model):
		self.view = view
		self.model = model
		#self.model.register_observer(self)
		self.view.button.clicked.connect( self.load_image )

	def load_image(self):
		options = QFileDialog.Options()
		filePath, _ = QFileDialog.getOpenFileName(
			self.view,
			"QFileDialog.getOpenFileName()",
			"",
			"PNG Files (*.png);;All Files (*)",
			options=options )
		if filePath:
			self.view.set_image(filePath)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	
	image_path = "D:\\Dropbox\\neal\\portfolio\\pnggcode\\assets\\test\\test_draw_four_color_png.png"
	colors = get_colors(image_path)  # from your existing code
	model = ColorTree(colors)
	
	view = InterfaceView()
	presenter = ImagePresenter(view, model)
	
	view.show()
	sys.exit(app.exec_())
