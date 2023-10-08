import numpy as np
import cv2


def find_color_contours(img_rgb, colors, svg_width):
	num_rows = len(img_rgb[0])
	num_cols = len(img_rgb)
	num_px = num_rows*num_cols
	print(f"Num pixels = {num_rows} x {num_cols} = {num_px}")
	print(f"Num colors = {len(colors)} = {(100*len(colors))//num_px} %")

	contours_by_color = []
	total_contours = 0
	coord_scale = svg_width/num_rows

	for color in colors:
		mask = make_mask(img_rgb, color)
		contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		scaled_contours = format_coords(contours, coord_scale)
		contours_by_color.append(scaled_contours)

		total_contours += len(scaled_contours)
		print(f"Color {len(contours_by_color)} / {len(colors)}, added {len(scaled_contours)} contours")
	print(f"Total contours = {total_contours}")
	return contours_by_color


def make_mask(img, color):
	mask = []
	for row in img:
		mask_row = []
		for pxl in row:
			if tuple(pxl) == color:
				mask_row.append(255)
			else:
				mask_row.append(0)
		mask.append(np.array(mask_row, dtype='uint8'))
	return np.array(mask)


def format_coords(contour_group, coord_scale):
	formatted_group = []
	for contour in contour_group:
		float_contour = []
		for pt in contour:
			pt = pt[0]
			pt_xy = tuple([coord_scale*float(xi) for xi in pt])
			float_contour.append(pt_xy)
		formatted_group.append(float_contour)
	return formatted_group
