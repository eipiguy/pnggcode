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