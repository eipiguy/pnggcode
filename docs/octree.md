# Octree

A nested tree dividing 3d space into levels of octants.

## Coordinates

Each node is given a "coordinate ID" to match which octant it is in for its current "family", or level of the tree.

For instance, if the split point for the initial level into octants was at $\mathbf{p} = (p_x, p_y, p_z)$, then the octants themselves would be labelled with coordinates where "less than" is indicated with a `0`, and "at least" is indicated with a `1`.

In this scheme, three dimensions gives three characters for each coordinate. The following IDs, for example, would define the associated sets,

`000` = $\{ (x,y,z) | \quad x < p_x, \quad y < p_y, \quad z < p_z \}$,

`001` = $\{ (x,y,z) | \quad x < p_x, \quad y < p_y, \quad z \ge p_z \}$,

`010` = $\{ (x,y,z) | \quad x < p_x, \quad y \ge p_y, \quad z < p_z \}$,

`011` = $\{ (x,y,z) | \quad x < p_x, \quad y \ge p_y, \quad z \ge p_z \}$,

and so on.

There are eight of these octants for each level of the tree (hence the name). This comes from dividing 3D space into 2 pieces for every dimension $(2^3 = 8)$.

In 2D, this would be indices with two characters instead of three, and give "quadrants" instead of octants.

A more general notion is called a "kd tree", as in a "k dimensional" tree, if you want to google.

## Directions

If the coordinates of the octants are like points, then the direction ids between them are like lines.
