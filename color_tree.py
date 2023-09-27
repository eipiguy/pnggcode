from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex

from octree import Octree


class TreeNode:
	def __init__(self, data, parent=None):
		self.data = data
		self.parent = parent
		self.children = []


class TreeModel( QAbstractItemModel ):
	def __init__( self, color_set ):
		super( TreeModel, self ).__init__()
		self.root = self.populate_nodes( color_set )


	def populate_nodes( self, color_set ):
		self.color_octree = Octree( color_set )
		print()
		pass


	def index( self, row, column, parent = QModelIndex() ):
		# return index to root node if parent not valid
		if not parent.isValid():
			return self.createIndex( row, column, self.root.children[row] )

		# otherwise return the specified child of the parent
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
		if parent_node == self.root:
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


	def data(self, index, role=Qt.DisplayRole):
		if not index.isValid():
			return None

		node = index.internalPointer()
		if role == Qt.DisplayRole:
			return node.data
