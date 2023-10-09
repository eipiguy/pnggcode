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
				print(f"Cell '{cell_id}' does not exist!")
				print(f"Could not find '{coords}' at '{cur_id}'.")
				print(f"Returning...")
				return
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

		# Point one cell at the same level
		# in each of the 9 directions
		ids = []
		directions = cube_directions()

		# resolve each neighbor direction
		for direction in directions:
			neighbor_id, remainder = resolve_direction( cell_id, direction )
			ids.append( [ neighbor_id, remainder ] )
		
		return ids


	def neighbors( self, cell_id ):

		# Point one cell at the same level
		# in each of the 9 directions
		ids = []
		neighbors = []
		directions = cube_directions()

		# resolve each neighbor direction
		for direction in directions:
			neighbor_id, remainder = resolve_direction( cell_id, direction )
			ids.append( [ neighbor_id, remainder ] )
			neighbor = self.get_cell( neighbor_id )
			if neighbor != None:
				neighbors.append( neighbor )
				neighbor = None

		return neighbors

# def id_direction( source_id, dest_id ):
# 
# 	# input are a list of coords for each cell
# 	source_coords = source_id.split()
# 	dest_coords = dest_id.split()
# 	direction_id = ''
# 
# 	# for now, we only compare where there is data for both
# 	# later I may be able to give finer resolution
# 	min_lvl = min( len(source_coords), len(dest_coords) )
# 	for id_lvl in range(min_lvl):
# 
# 		# a tuple of coords for each
# 		source_lvl_coords = source_coords[id_lvl]
# 		dest_lvl_coords = dest_coords[id_lvl]
# 
# 		# directions are space delimeted tuples 
# 		lvl_direction = '' if direction_id == '' else ' '
# 		for i,elem in enumerate(source_lvl_coords):
# 			# they need tuple commas
# 			# to identify negative values
# 			if i != 0:
# 				lvl_direction += ','
# 
# 			source_val = int( source_lvl_coords[i] )
# 			dest_val = int( dest_lvl_coords[i] )
# 			direction_val = dest_val - source_val
# 			lvl_direction += str( direction_val )
# 
# 		direction_id += lvl_direction
# 
# 	return direction_id


def cube_directions( dimensions = 3 ):
	alphabet = [ '-1', '0', '1' ]
	delimeter = ','
	cur_ids = [ '' ]
	for d in range(dimensions):
		# branch from all current words
		next_ids = []
		for id_fragment in cur_ids:
			# add all possible tags
			for a in alphabet:
				prefix = id_fragment
				if prefix != '':
					prefix += delimeter
				next_ids.append( prefix + a )
		cur_ids = next_ids

	# delete self id
	self_id = '0,' * dimensions
	self_id = self_id[:-1]
	next_ids.remove( self_id )
	return next_ids


def resolve_direction( source, direction ):
	source_coords = source.split()
	dimensions = len( source_coords[0] )

	destination = []
	carry = [ int(x) for x in direction.split(',') ]
	for coords in reversed(source_coords):

		destination_lvl = ''
		for j,elem in enumerate(coords):

			# compute result using previous remainder
			result = int(elem) + carry[j]

			# adjust result using new remainder
			carry[j] = 0
			if result < 0:
				carry[j] = result
				result = 1
			elif result > 1: # must be == 2 in this case
				carry[j] = result - 1
				result = 0
			destination_lvl += str(result)

		destination.append(destination_lvl)

	destination = reversed(destination)

	return ' '.join(destination), ','.join([ str(r) for r in carry])


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
