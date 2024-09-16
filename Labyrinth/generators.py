import random
import math


def _minmax(num, min, max):
	if num < min:
		return min
	if num > max:
		return max
	return num


def _get_starting_box(width: int, height: int) -> list:
	"""
	:return: A matrix with an empty field.
	2 - a wall, 1 - a blocked tile, 0 - empty tile
	"""
	field = [[2 for x in range(width)] for y in range(height)]
	for y in range(1, height - 1):
		for x in range(1, width - 1):
			field[y][x] = 1
	return field


def _get_random_exits(width: int, height: int, exits: int) -> set:
	"""
	:return: A set of random finish cords - (x, y)
	"""
	
	if exits > width * 2 + height * 2 - 8:
		exits = width * 2 + height * 2 - 8
	elif exits <= 0:
		exits = 1
	
	possible_cords = []
	for y in range(1, height - 1):
		possible_cords.append((0, y))
		possible_cords.append((width - 1, y))
	for x in range(1, width - 1):
		possible_cords.append((x, 0))
		possible_cords.append((x, height - 1))
	
	finishes = set()
	i = 0
	while possible_cords and i < exits:
		random_finish = random.randint(0, len(possible_cords) - 1)
		finishes.add(possible_cords.pop(random_finish))
		
		i += 1
	
	return finishes


def _generation_cycle(next_gen: list, priority_index: int, random_choice_chance: int, dead_end_chance: int,
                      guaranteed_generations: int):
	# Four different loops for optimisation, looks bad maybe refactor
	if random_choice_chance and dead_end_chance:
		while next_gen:
			if random.randint(1, 100) <= random_choice_chance:
				chosen_index = random.randint(0, len(next_gen) - 1)
			else:
				chosen_index = priority_index
			
			if guaranteed_generations > 0:
				guaranteed_generations -= 1
				next_gen.pop(chosen_index)()
			elif random.randint(1, 100) <= dead_end_chance:
				next_gen.pop(chosen_index)  # Just delete and not generate
			else:
				next_gen.pop(chosen_index)()
	elif random_choice_chance:
		while next_gen:
			if random.randint(1, 100) <= random_choice_chance:
				next_gen.pop(random.randint(0, len(next_gen) - 1))()
			else:
				next_gen.pop(priority_index)()
	elif dead_end_chance:
		while next_gen:
			if guaranteed_generations > 0:
				guaranteed_generations -= 1
				next_gen.pop(priority_index)()
			elif random.randint(1, 100) <= dead_end_chance:
				next_gen.pop(priority_index)
			else:
				next_gen.pop(priority_index)()
	else:
		while next_gen:
			next_gen.pop(priority_index)()


def gen_end(field: list, field_width: int, field_height: int, endX: int, endY: int, startX: int, startY: int):
	"""
	Connects an end to a generated maze
	"""
	if endX == 0:
		move = (1, 0)
		to_mine = field_width - 2
	elif endX == field_width - 1:
		move = (-1, 0)
		to_mine = field_width - 2
	elif endY == 0:
		move = (0, 1)
		to_mine = field_height - 2
	else:
		move = (0, -1)
		to_mine = field_height - 2
	
	for _ in range(to_mine):
		endX += move[0]
		endY += move[1]
		
		if field[endY][endX] == 0:
			return
		
		field[endY][endX] = 0
	# Exit didn't connect with a maze
	angle = math.degrees(math.atan2(startY - endY, startX - endX))
	angle = round(angle, 2)
	if angle % 15 == 0:
		angle += 1
	spawn_path = generator_precise(endX, endY, angle, max_x=field_width, max_y=field_height)
	for x, y in spawn_path:
		xx, yy = round(x), round(y)
		if field[yy][xx] == 0:
			if xx == endX or yy == endY:
				continue
			return
		field[yy][xx] = 0


def generator_precise(x: int, y: int, angle: float,
                      max_x: float = float("inf"), max_y: float = float("inf"), min_x: float = 0, min_y: float = 0,
                      max_path_len: float = float("inf")) -> (float, float):
	"""
	Generator to go through a matrix at an angle
	"""
	
	rad_angle = math.radians(angle)
	delta_x = math.cos(rad_angle)
	delta_y = math.sin(rad_angle)
	
	rounding_fix = 0.5000000001  # Float number could break, then change it closer to 0.5 (0.501)
	
	max_x -= rounding_fix  # So that these numbers never would round up higher than max index
	max_y -= rounding_fix
	
	if delta_x > 0:
		next_x = round(x) + rounding_fix
		x_steps = (max_x - x) / delta_x
		next_x_step = 1
	elif delta_x < 0:
		next_x = round(x) - rounding_fix
		x_steps = (x - min_x) / -delta_x
		next_x_step = -1
	else:
		x_steps = float("inf")
		next_x = round(x) - rounding_fix
		next_x_step = -1
	
	if delta_y > 0:
		next_y = round(y) + rounding_fix
		y_steps = (max_y - y) / delta_y
		next_y_step = 1
	elif delta_y < 0:
		next_y = round(y) - rounding_fix
		y_steps = (y - min_y) / -delta_y
		next_y_step = -1
	else:
		y_steps = float("inf")
		next_y = round(y) + rounding_fix
		next_y_step = 1
	
	total_steps = min(x_steps, y_steps, max_path_len)
	
	if angle % 45 == 0:
		for _ in range(math.ceil(total_steps)):
			yield x, y
			x += delta_x
			y += delta_y
		return
	
	step = 0
	while step < total_steps:
		yield x, y
		
		x_step = abs((x - next_x) / delta_x)
		y_step = abs((y - next_y) / delta_y)
		if x_step < y_step:
			min_step = x_step
			next_x += next_x_step
		else:
			min_step = y_step
			next_y += next_y_step
		x += delta_x * min_step
		y += delta_y * min_step
		step += min_step


def generate_field_original_optimised(field_width: int, field_height: int, exits: int = 1) -> (list, int, int):
	"""
	More blocky generation, has a lot of strange 1 block paths, kinda easy to predict on small sizes.
	4.9s for 1024x1024
	:return: A field, start X and Y.
	"""
	
	def get_path(x, y, side) -> (int, int):
		if side == 'left':
			ret_x, ret_y = x - 1, y
			check_x = (-1, 0)
			check_y = (-1, 1)
		elif side == 'right':
			ret_x, ret_y = x + 1, y
			check_x = (0, 1)
			check_y = (-1, 1)
		elif side == 'up':
			ret_x, ret_y = x, y - 1
			check_x = (-1, 1)
			check_y = (-1, 0)
		elif side == 'down':
			ret_x, ret_y = x, y + 1
			check_x = (-1, 1)
			check_y = (0, 1)
		else:
			return False
		
		if field[ret_y][ret_x] != 1:
			return False
		
		for xd in range(check_x[0], check_x[1] + 1):
			for yd in range(check_y[0], check_y[1] + 1):
				if field[yd + ret_y][xd + ret_x] == 0:
					return False
		return ret_x, ret_y
	
	def generate_path(pointX, pointY, *sides):
		nonlocal field, next_gen
		
		for side in sides:
			pathcords = get_path(pointX, pointY, side)
			if pathcords:
				pathX, pathY = pathcords
				field[pathY][pathX] = 0
				next_gen.append(lambda: generate_path(pathX, pathY, 'left'))
				next_gen.append(lambda: generate_path(pathX, pathY, 'right'))
				next_gen.append(lambda: generate_path(pathX, pathY, 'up'))
				next_gen.append(lambda: generate_path(pathX, pathY, 'down'))
	
	field = _get_starting_box(field_width, field_height)
	
	startX, startY = random.randint(1, field_width - 2), random.randint(1, field_height - 2)
	
	finishes = _get_random_exits(field_width, field_height, exits)
	
	field[startY][startX] = 0
	for endX, endY in finishes:
		field[endY][endX] = 3
	
	# Generation
	next_gen = [lambda: generate_path(startX, startY, 'down'), lambda: generate_path(startX, startY, 'left'),
	            lambda: generate_path(startX, startY, 'right'), lambda: generate_path(startX, startY, 'up')]
	while next_gen:
		index = random.randint(0, len(next_gen) - 1)
		next_gen.pop(index)()
	
	for endX, endY in finishes:
		gen_end(field, field_width, field_height, endX, endY, startX, startY)
	
	# Change values for return
	for y in range(field_height):
		field[y][0] = 1
		field[y][field_width - 1] = 1
	for x in range(field_width):
		field[0][x] = 1
		field[field_height - 1][x] = 1
	for endX, endY in finishes:
		field[endY][endX] = 2
	
	return field, startX, startY


def generate_field_original(fieldX: int, fieldY: int, exits: int = 1) -> (list, int, int):
	"""
	Squiggly generation, not that hard to predict, paths change direction a lot. Also kinda cool for strange sizes.
	Very random generation speed, realistically O(n^3). 40s for 1024x1024
	Works similarly to dfs.
	:return: A field, start X and Y.
	"""
	
	def get_path(x, y, side):
		if side == 'left':
			ret_x, ret_y = x - 1, y
			check_x = (-1, 0)
			check_y = (-1, 1)
		elif side == 'right':
			ret_x, ret_y = x + 1, y
			check_x = (0, 1)
			check_y = (-1, 1)
		elif side == 'up':
			ret_x, ret_y = x, y - 1
			check_x = (-1, 1)
			check_y = (-1, 0)
		elif side == 'down':
			ret_x, ret_y = x, y + 1
			check_x = (-1, 1)
			check_y = (0, 1)
		else:
			return False
		
		if field[ret_y][ret_x] != 1:
			return False
		
		for xd in range(check_x[0], check_x[1] + 1):
			for yd in range(check_y[0], check_y[1] + 1):
				if field[yd + ret_y][xd + ret_x] == 0:
					return False
		return ret_x, ret_y
	
	def generate_path_new(pointX, pointY, *sides):
		nonlocal field, next_gen
		if 'all' in sides:
			sides = ["left", "right", "up", "down"]
		
		random.shuffle(sides)
		paths = []
		for side in sides:
			pathcords = get_path(pointX, pointY, side)
			if pathcords:
				pathX, pathY = pathcords
				paths.append((pathX, pathY))
		
		# Dead ends are the ends that are dead
		if not paths:
			return
		
		for pathX, pathY in paths:
			field[pathY][pathX] = 0
			next_gen.insert(0, lambda: generate_path_new(pathX, pathY, 'all'))
			break
		next_gen.insert(0, lambda: generate_path_new(pointX, pointY, 'all'))
	
	field = _get_starting_box(fieldX, fieldY)
	
	startX, startY = random.randint(1, fieldX - 2), random.randint(1, fieldY - 2)
	
	finishes = _get_random_exits(fieldX, fieldY, exits)
	
	field[startY][startX] = 0
	for endX, endY in finishes:
		field[endY][endX] = 3
	
	next_gen = [lambda: generate_path_new(startX, startY, 'all')]
	
	shuffle_threshold = fieldY * fieldX // 10
	while next_gen:
		next_gen[0]()
		next_gen.pop(0)
		
		if len(next_gen) > shuffle_threshold and random.randint(1, 20) == 1:
			random.shuffle(next_gen)
	
	for endX, endY in finishes:
		gen_end(field, fieldX, fieldY, endX, endY, startX, startY)
	
	# Just for return
	for y in range(fieldY):
		field[y][0] = 1
		field[y][fieldX - 1] = 1
	for x in range(fieldX):
		field[0][x] = 1
		field[fieldY - 1][x] = 1
	for endX, endY in finishes:
		field[endY][endX] = 2
	
	return field, startX, startY


def generate_field_custom(field_width: int, field_height: int, exits: int = 1,
                          weight_left: int = 1, weight_right: int = 1, weight_up: int = 1,
                          centered_spawn: bool = False, bfs: bool = False, random_node_chance: int = 0,
                          dead_end_chance: int = 0, guaranteed_generations: int = 10) -> (list, int, int):
	"""
	Customisable, slower than generate_field_original_optimised, but can have a lot of variety.
	5.5s for 1024x1024 (way slower with random nodes - 10s)
	
	Weights are relative to where we are generating - if left is the highest weight, the labyrinth will steer to the left.
	There is no weight_down because we never generate down - it is backwards, and is always already used.
	
	:param exits: How many exits are there, will correct impossible values.
	:param weight_left: Generation will steer to the left, can generate in a spiral.
	:param weight_right: Same but right.
	:param weight_up: Generation will be more linear, can create very block generation.
	:param centered_spawn: No random spawn location - always at a field center.
	:param bfs: True - BFS generation, False - DFS
	DFS generates faster, generates from last generated nodes, generally leads to 1 long path and few branches.
	BFS generates from first nodes, mostly creates same fields.
	:param random_node_chance: What percentage of node generations should be chosen NOT on BFS or DFS but random.
	:param dead_end_chance: Chance to not generate further at any point.
	:param guaranteed_generations: How many generations will never be dead ends.
	:return: A field, start X and Y.
	"""
	
	def get_path(x, y, side) -> (int, int):
		if side == 'left':
			ret_x, ret_y = x - 1, y
			check_x = (-1, 0)
			check_y = (-1, 1)
		elif side == 'right':
			ret_x, ret_y = x + 1, y
			check_x = (0, 1)
			check_y = (-1, 1)
		elif side == 'up':
			ret_x, ret_y = x, y - 1
			check_x = (-1, 1)
			check_y = (-1, 0)
		elif side == 'down':
			ret_x, ret_y = x, y + 1
			check_x = (-1, 1)
			check_y = (0, 1)
		else:
			return False
		
		if field[ret_y][ret_x] != 1:
			return False
		
		for xd in range(check_x[0], check_x[1] + 1):
			for yd in range(check_y[0], check_y[1] + 1):
				if field[yd + ret_y][xd + ret_x] == 0:
					return False
		return ret_x, ret_y
	
	def generate_path(pointX, pointY, *sides):
		nonlocal field, next_gen
		
		for side in sides:
			pathcords = get_path(pointX, pointY, side)
			
			if pathcords:
				# I deleted relative down, because it will always be already used - we came from there
				if side == "up":
					relative_sides = ["right", "up", "left"]
				elif side == "left":
					relative_sides = ["up", "left", "down"]
				elif side == "down":
					relative_sides = ["left", "down", "right"]
				else:
					relative_sides = ["down", "right", "up"]
				
				randomised_sides = []
				weights = [weight_right, weight_up, weight_left]
				for _ in range(3):
					index = random.choices(range(len(relative_sides)), weights, k=1)[0]
					randomised_sides.append(relative_sides[index])
					relative_sides.pop(index)
					weights.pop(index)
				
				pathX, pathY = pathcords
				field[pathY][pathX] = 0
				
				next_gen.append(lambda: generate_path(pathX, pathY, randomised_sides[2]))
				next_gen.append(lambda: generate_path(pathX, pathY, randomised_sides[1]))
				next_gen.append(lambda: generate_path(pathX, pathY, randomised_sides[0]))
	
	field = _get_starting_box(field_width, field_height)
	
	if centered_spawn:
		startX, startY = field_width // 2, field_height // 2
	else:
		startX, startY = random.randint(1, field_width - 2), random.randint(1, field_height - 2)
	
	finishes = _get_random_exits(field_width, field_height, exits)
	
	field[startY][startX] = 0
	for endX, endY in finishes:
		field[endY][endX] = 3
	
	# Generation
	next_gen = [lambda: generate_path(startX, startY, 'left'), lambda: generate_path(startX, startY, 'up'),
	            lambda: generate_path(startX, startY, 'right'), lambda: generate_path(startX, startY, 'down')]
	
	if bfs:
		priority_index = 0
	else:
		priority_index = -1
	
	next_gen.pop(random.randint(0, 3))()
	_generation_cycle(next_gen, priority_index, random_node_chance, dead_end_chance, guaranteed_generations)
	
	for endX, endY in finishes:
		gen_end(field, field_width, field_height, endX, endY, startX, startY)
	
	# Change values for return
	for y in range(field_height):
		field[y][0] = 1
		field[y][field_width - 1] = 1
	for x in range(field_width):
		field[0][x] = 1
		field[field_height - 1][x] = 1
	for endX, endY in finishes:
		field[endY][endX] = 2
	
	return field, startX, startY


def generate_spiral(field_width: int, field_height: int, exits: int = 1,
                    steer_strength: int = 500, forward_strength: int = 100, centered_spawn: bool = False,
                    random_node_percentage: int = 5):
	"""Specific configuration of weighted generation, labyrinth will look like a spiral.
	:param steer_strength: How strong should a spiral steer to a side, in percentage
	:param forward_strength: The higher this value is - the more blocky an algorithm will be.
	:param centered_spawn: If we should always start from a center.
	:param random_node_percentage: How often a random node will be chosen, help in creating more branches.
	"""
	if random.randint(0, 1):
		return generate_field_custom(field_width, field_height, exits, centered_spawn=centered_spawn,
		                             weight_up=forward_strength, weight_right=steer_strength, weight_left=100,
		                             random_node_chance=random_node_percentage)
	else:
		return generate_field_custom(field_width, field_height, exits, centered_spawn=centered_spawn,
		                             weight_up=forward_strength, weight_left=steer_strength, weight_right=100,
		                             random_node_chance=random_node_percentage)


def generate_spiral_long(field_width: int, field_height: int, exits: int = 1):
	"""Specific configuration of weighted generation, labyrinth will look like a defined spiral with long corridors."""
	if random.randint(0, 1):
		return generate_field_custom(field_width, field_height, exits, centered_spawn=False,
		                             weight_up=1000, weight_right=1000, weight_left=1)
	else:
		return generate_field_custom(field_width, field_height, exits, centered_spawn=False,
		                             weight_up=1000, weight_left=1000, weight_right=1)


def generate_corridors_long(field_width: int, field_height: int, exits: int = 1):
	"""Specific configuration of weighted generation, labyrinth will look like a defined spiral with long corridors."""
	if random.randint(0, 1):
		return generate_field_custom(field_width, field_height, exits, centered_spawn=False,
		                             weight_up=100, weight_right=1, weight_left=1, random_node_chance=10)
	else:
		return generate_field_custom(field_width, field_height, exits, centered_spawn=False,
		                             weight_up=100, weight_left=1, weight_right=1, random_node_chance=10)


def generate_corridors_small(field_width: int, field_height: int, exits: int = 1):
	"""Specific configuration of weighted generation, labyrinth will look like a defined spiral with long corridors."""
	if random.randint(0, 1):
		return generate_field_custom(field_width, field_height, exits, centered_spawn=False,
		                             weight_up=100, weight_right=1, weight_left=1, random_node_chance=40)
	else:
		return generate_field_custom(field_width, field_height, exits, centered_spawn=False,
		                             weight_up=100, weight_left=1, weight_right=1, random_node_chance=40)


def generate_diagonal(field_width: int, field_height: int, exits: int = 1, steer_strength: int = 500,
                      centered_spawn: bool = False, random_node_percentage: int = 20):
	"""Specific configuration of weighted generation.
	High steer strength will make labyrinth more diagonal, low steer strength will make it more horizontal (try 10)
	:param steer_strength: How strong should a spiral steer to a side, in percentage
	:param centered_spawn: If we should always start from a center.
	:param random_node_percentage: How often a random node will be chosen, help in creating more branches.
	"""
	return generate_field_custom(field_width, field_height, exits, centered_spawn=centered_spawn,
	                             weight_up=100, weight_right=steer_strength, weight_left=steer_strength,
	                             random_node_chance=random_node_percentage)


def generate_field_vector(field_width: int, field_height: int,
                          wall_width: int = 1, path_width: int = 1,
                          max_path_len: float = float("inf"), min_path_len: float = 1,
                          check_angle_step: int = 90, ignore_tiles_radius: int = 3,
                          exits: int = 1, centered_spawn: bool = False, bfs: bool = False,
                          random_choice_chance: int = 0,
                          dead_end_chance: int = 0, guaranteed_generations: int = 10) -> (list, int, int):
	"""
	O(n^2), 5.6s for 128x128; 26s for 256x256
	:param exits: How many exits are there, will correct impossible values.
	:param centered_spawn: No random spawn location - always at a field center.
	:param bfs: True - BFS generation, False - DFS
	DFS generates faster, generates from last generated nodes, generally leads to 1 long path and few branches.
	BFS generates from first nodes, mostly creates same fields.
	:param random_choice_chance: What percentage of node generations should be chosen NOT on BFS or DFS but random.
	:return: A field, start X and Y.
	"""
	
	def check_angle(x, y, angle, ignore_tiles: set = None) -> bool:
		"""
		Changes given ignore_tiles
		:return: If we touch another path in front
		"""
		
		if ignore_tiles is None:
			ignore_tiles = set()
		
		ignore_tiles.add((round(x), round(y)))
		
		# We iterate over all angles clockwise in a circle, to check if there are already other paths
		# within wall_width, which would be too close (wall_width)
		for check_angle in range(angle - 90, angle + 90, 5):
			path = generator_precise(x, y, check_angle, field_width, field_height, 1, 1, max_path_len=wall_width + 1)
			for float_check_x, float_check_y in path:
				check_x, check_y = round(float_check_x), round(float_check_y)
				
				if (check_x, check_y) in ignore_tiles:
					continue
				
				if field[check_y][check_x] != 1:
					return True
				
				ignore_tiles.add((check_x, check_y))
		return False
	
	def check_path_by_angle(check_x: int, check_y: int, angle: float, ignore_tiles: set = None) -> bool:
		"""
		:return: If a path to this angle would be bigger than min_path_len
		"""
		if ignore_tiles is None:
			ignore_tiles = set()
		
		# Checking an angle if it can become a path
		# So we iterate over all indexes that would be that path
		for float_x, float_y in generator_precise(check_x, check_y, angle, field_width, field_height, 0, 0,
		                                          max_path_len=max_path_len):
			if not check_angle(float_x, float_y, angle, ignore_tiles):
				continue
			
			wall_len = math.sqrt((check_x - float_x) ** 2 + (check_y - float_y) ** 2)
			
			if wall_len >= min_path_len:
				return True
			else:
				return False
		return True
	
	def generate_path(start_x, start_y, ignore_tiles: set = None):
		nonlocal field, next_gen
		
		if field[start_y][start_x] != 0:
			return
		
		if ignore_tiles is None:
			ignore_tiles_close = {(start_x, start_y)}
		else:
			# You can make an easier equation to make it faster - for example just start_x - x <= ignore_radius
			ignore_tiles_close = {(x, y) for x, y in ignore_tiles if
			                      math.sqrt((start_x - x) ** 2 + (start_y - y) ** 2) <= ignore_tiles_radius}
		
		possible_angles = [[0, None]]
		group = 0
		# Finding possible angles to generate
		for angle in range(0, 360, check_angle_step):
			if check_path_by_angle(start_x, start_y, angle, ignore_tiles_close):
				if possible_angles[group][1] is None:
					possible_angles[group][0] = angle
				possible_angles[group][1] = angle
				continue
			elif possible_angles[group][1] is not None:
				group += 1
				possible_angles.append([0, None])
		
		if possible_angles[-1][1] is None:
			possible_angles.pop()
			if not possible_angles:
				return
		
		chosen_restrains = random.randint(0, len(possible_angles) - 1)
		chosen_angle = random.randint(possible_angles[chosen_restrains][0], possible_angles[chosen_restrains][1])
		
		i = 0  # Retries
		while chosen_angle % 90 == 45:
			chosen_restrains = random.randint(0, len(possible_angles) - 1)
			chosen_angle = random.randint(possible_angles[chosen_restrains][0], possible_angles[chosen_restrains][1])
			if i > 5:
				return
			i += 1
		
		new_ignore_tiles = set()
		new_ignore_tiles.add((start_x, start_y))
		current_path_len = 0
		# Generating a wall at chosen angle
		for float_x, float_y in generator_precise(start_x, start_y, chosen_angle, field_width, field_height, 1, 1,
		                                          max_path_len=max_path_len):
			x, y = round(float_x), round(float_y)
			ignore_tiles_close.add((x, y))
			
			if check_angle(float_x, float_y, chosen_angle, ignore_tiles_close):
				break
			
			new_ignore_tiles.add((x, y))
			
			if field[y][x] == 1:
				field[y][x] = 0
				
				if current_path_len > wall_width:
					next_gen.append(lambda cx=x, cy=y: generate_path(cx, cy, new_ignore_tiles))
					current_path_len -= wall_width
			current_path_len += 1
	
	field = _get_starting_box(field_width, field_height)
	
	if centered_spawn:
		startX, startY = field_width // 2, field_height // 2
	else:
		startX, startY = random.randint(1, field_width - 2), random.randint(1, field_height - 2)
	field[startY][startX] = 0
	
	finishes = _get_random_exits(field_width, field_height, exits)
	for endX, endY in finishes:
		field[endY][endX] = 3
	
	path_width = _minmax(path_width, 1, field_width - wall_width)
	wall_width = _minmax(wall_width, 1, field_width - path_width)
	
	# Generation
	next_gen = []
	
	if bfs:
		priority_index = 0
	else:
		priority_index = -1
	generate_path(startX, startY)  # Calls first generation here because there is a chance to not generate later
	
	_generation_cycle(next_gen, priority_index, random_choice_chance, dead_end_chance, guaranteed_generations)
	
	for endX, endY in finishes:
		gen_end(field, field_width, field_height, endX, endY, startX, startY)
	
	# Change values for return
	for y in range(field_height):
		field[y][0] = 1
		field[y][field_width - 1] = 1
	for x in range(field_width):
		field[0][x] = 1
		field[field_height - 1][x] = 1
	for endX, endY in finishes:
		field[endY][endX] = 2
	field[startY][startX] = 0
	
	return field, startX, startY


if __name__ == '__main__':
	import time
	
	tries = 100
	size = 4
	while size < 1000:
		size *= 2
		width = height = size
		times = []
		for _ in range(tries):
			s = time.time()
			# generate_field_chaos(width, height, wall_width=2, path_width=1, min_path_len=3, check_angle_step=15,
			#                      centered_spawn=True)
			# generate_field_chaos(width, height, dead_end_chance=50, random_choice_chance=50)
			generate_field_custom(width, height, dead_end_chance=100, random_node_chance=100)
			times.append(time.time() - s)
		
		print(size, times)
		print(sum(times) / len(times))
		print()

# TODO: aChaos generator still isn't complete and doesn't use wall and path width correctly
# same with other parameters
# TODO: use numpy to make labyrinths faster ? both here and in main.py
# another optimisation - commands are stored in a list, it is O(n) for deletetion for random indexes, change it for self balancing binary tree ?
# (test)

# reversed chaos (just generate a chaos, then reverse walls and empty tiles, you will (probably) get a lot of unconnected rooms
# just go through an array, when you see this room - connect it randomly with any already connected room.

# instead of centered_spawn make it just a (spawn_x, spawn_y), so you can choose
# add an ability to go diagonally ? and change the game, obviously
