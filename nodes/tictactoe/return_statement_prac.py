def get_upper_and_lower(): #gets coordinates for each square for top and bottom corners
	lower_corner_height, lower_corner_width = 4, 6
	upper_corner_height, upper_corner_width = 5, 7
	return [lower_corner_height, lower_corner_width, upper_corner_height, upper_corner_width]

print(get_upper_and_lower()[0])
