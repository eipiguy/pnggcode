def median_vals( points ):

	points = list(points)
	num_points = len(points)
	if num_points == 0:
		return None

	med_id = num_points // 2
	dimensions = len(points[0])

	component_vals = [ [] for _ in range(dimensions) ]
	for pt in points:
		for d in range(dimensions):
			component_vals[d].append(pt[d])

	component_medians = []
	for d in range(dimensions):
		sorted_vals = sorted(component_vals[d])
		if num_points % 2 == 0:
			median = ( sorted_vals[med_id - 1] + sorted_vals[med_id] ) / 2
		else:
			median = sorted_vals[med_id]
		component_medians.append( median )

	return component_medians


class Octree:

	MIN_POINTS = 1

	def __init__( self, points, octree_id = '' ):
		self.id = octree_id
		self.points = set(points)
		# if at the minimum granularity,
		# stop before octant initialization
		if len(self.points) <= self.MIN_POINTS:
			return

		# if more than the minimum granularity,
		# split into eight children and sort
		octant_points = self.sort_into_octants( self.points )
		self.initialize_octant_trees( octant_points )


	def sort_into_octants( self, points ):
		octant_points = {
				'000': [],
				'001': [],
				'010': [],
				'011': [],
				'100': [],
				'101': [],
				'110': [],
				'111': []
			}
		self.split_point = median_vals( points )
		for pt in self.points:
			octant_points[ self.get_split_id(pt) ].append( pt )

		return octant_points


	def initialize_octant_trees( self, octant_points ):
		self.octants = {}
		id_prefix = ''
		for corner_id in octant_points:
			if len(octant_points[corner_id]) == 0:
				continue

			# If not the root, prepend parent id
			if self.id != '':
				id_prefix = self.id + ' '

			# a sub-tree for each populated octant
			self.octants[corner_id] = Octree( octant_points[corner_id], id_prefix + corner_id )


	def get_split_id( self, point ):
		id = ''.join([ '0' if x < self.split_point[i] else '1' for i,x in enumerate(point) ])
		return id


	def roll_call( self ):
		members = {
			self.id: self.points
		}

		if hasattr( self, 'octants' ):
			for corner_id in self.octants:
				corner = self.octants[corner_id]
				child_roll = corner.roll_call()
				for id in child_roll:
					members[id] = child_roll[id]

		return members


	def get_cell( self, cell_id ):
		cell_coords = cell_id.split()
		cur_cell = self
		cur_id = ''
		for coords in cell_coords:
			if hasattr( cur_cell, 'octants' ) and coords in cur_cell.octants:
				cur_id += coords
				cur_cell = cur_cell.octants[coords]
			else:
				print(f"Could not find cell '{cell_id}'")
				print(f"Error at '{cur_id}' finding '{coords}'")
				print(f"Returning '{cur_id}'")
				break
		return cur_cell


	def sibling_coords( self, cell_id ):
		cell_coords = cell_id.split()
		parent_coords = ' '.join( cell_coords[:-1] )
		child_local_coords = cell_coords[-1]

		siblings = []
		parent_cell = self.get_cell( parent_coords )
		for octant_coords in parent_cell.octants:
			if octant_coords != child_local_coords:
				siblings.append( parent_cell.octants[octant_coords].id )
		return siblings 


	def neighbor_ids( self, cell_id ):
		cell_coords = cell_id.split()
		parent_coords = ' '.join( cell_coords[:-1] )
		child_local_coords = cell_coords[-1]

		# immediate siblings
		sibling_coords = self.sibling_coords( cell_id )

		# go through aunts/uncles
		parent_siblings = self.sibling_coords( parent_coords )
		for p_sibling_id in parent_siblings:
			directions = id_direction( p_sibling_id, parent_coords )

			# classify as edge, face, or corner
			# (Hamming distance)
			nonzeros = direction_nonzeros( directions )

			# get associated cousins



		#		- 3 are face neighbors with 4 cousins each
		#		- 3 are edge neighbors with 2 cousins each
		#		- 1 is the opposite corner with 1 cousin
		# Making a total of 26
		#	- 7 immediate siblings
		#	- 12 face cousins
		#	- 6 edge cousins
		#	- 1 corner cousin
			pass


def id_direction( source_id, dest_id ):

	# input are a list of coords for each cell
	source_coords = source_id.split()
	dest_coords = dest_id.split()
	direction_id = ''

	# for now, we only compare where there is data for both
	# later I may be able to give finer resolution
	min_lvl = min( len(source_coords), len(dest_coords) )
	for id_lvl in range(min_lvl):

		# a tuple of coords for each
		source_lvl_coords = source_coords[id_lvl]
		dest_lvl_coords = dest_coords[id_lvl]

		# directions are space delimeted tuples 
		lvl_direction = '' if direction_id == '' else ' '
		for i,elem in enumerate(source_lvl_coords):
			# they need tuple commas
			# to identify negative values
			if i != 0:
				lvl_direction += ','

			source_val = int( source_lvl_coords[i] )
			dest_val = int( dest_lvl_coords[i] )
			direction_val = dest_val - source_val
			lvl_direction += str( direction_val )

		direction_id += lvl_direction

	return direction_id


def resolve_direction( source, direction ):
	source_coords = source.split()
	directions = direction.split()

	destination = []
	for i,coords in enumerate(source_coords):

		destination_lvl = ''
		direction_elems = directions[i].split(',')

		for j,elem in enumerate(coords):
			result = int(elem) + int(direction_elems[j])
			if result < 0:
				result = 0
			elif result > 1:
				result = 1
			destination_lvl += str(result)

		destination.append(destination_lvl)

	return ' '.join(destination)


def direction_nonzeros( direction_string ):
	nonzero_direction_elems = 0

	# split the list of level directions
	directions = direction_string.split()
	for direction_lvl in directions:

		# split coords into list of elements
		lvl_elems = direction_lvl.split(',')

		for elem in lvl_elems:
			if elem != '0':
				nonzero_direction_elems += 1

	return nonzero_direction_elems