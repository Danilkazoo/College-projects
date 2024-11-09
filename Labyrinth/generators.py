import math
import random


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
	
	exits = _minmax(exits, 1, (width + height - 4) * 2)
	
	possible_cords = []
	for y in range(1, height - 1):
		possible_cords.append((0, y))
		possible_cords.append((width - 1, y))
	for x in range(1, width - 1):
		possible_cords.append((x, 0))
		possible_cords.append((x, height - 1))
	
	finishes = set()
	for i in range(exits):
		if not possible_cords:
			break
		random_finish = random.randint(0, len(possible_cords) - 1)
		finishes.add(possible_cords.pop(random_finish))
	
	return finishes


def _generation_cycle(next_gen: list, generation_function, priority_index: int, random_choice_chance: int,
                      dead_end_chance: int, guaranteed_generations: int):
	if random_choice_chance and dead_end_chance:
		while next_gen:
			if random.randint(1, 100) <= random_choice_chance:
				chosen_index = random.randint(0, len(next_gen) - 1)
			else:
				chosen_index = priority_index
			
			if guaranteed_generations > 0:
				guaranteed_generations -= 1
			elif random.randint(1, 100) <= dead_end_chance:
				next_gen.pop(chosen_index)
				continue
			generation_function(*next_gen.pop(chosen_index))
	elif random_choice_chance:
		while next_gen:
			if random.randint(1, 100) <= random_choice_chance:
				generation_function(*next_gen.pop(random.randint(0, len(next_gen) - 1)))
			else:
				generation_function(*next_gen.pop(priority_index))
	elif dead_end_chance:
		while next_gen:
			if guaranteed_generations > 0:
				guaranteed_generations -= 1
			elif random.randint(1, 100) <= dead_end_chance:
				next_gen.pop(priority_index)
				continue
			generation_function(*next_gen.pop(priority_index))
	else:
		while next_gen:
			generation_function(*next_gen.pop(priority_index))


def _gen_end(field: list, field_width: int, field_height: int, endX: int, endY: int, startX: int, startY: int):
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
	spawn_path = _generator_precise(endX, endY, angle, max_x=field_width, max_y=field_height)
	for x, y in spawn_path:
		xx, yy = round(x), round(y)
		if field[yy][xx] == 0:
			if xx == endX or yy == endY:
				continue
			return
		field[yy][xx] = 0


def _generator_precise(x: int, y: int, angle: float,
                       max_x: float = float("inf"), max_y: float = float("inf"), min_x: float = 0, min_y: float = 0,
                       max_path_len: float = float("inf"), skip_path: bool = False) -> (float, float):
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
	
	if skip_path:
		x += delta_x * total_steps - (rounding_fix * next_x_step)
		y += delta_y * total_steps - (rounding_fix * next_y_step)
		yield x, y
		return
	
	if angle % 45 == 0:  # I just copied simple gen
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


def _iterator_between_points(x1, y1, x2, y2):
	"""
	Starts from (x1, y1) and ends on (x2, y2), includes both
	"""
	angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
	distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
	yield from _generator_precise(x1, y1, angle, max_path_len=distance, max_x=float("inf"), max_y=float("inf"))


def generate_field_original(field_width: int, field_height: int, exits: int = 1) -> (list, int, int):
	"""
	More blocky generation, has a lot of strange 1 block paths, kinda easy to predict on small sizes.
	2.53s for 1024x1024
	:return: A field, start X and Y.
	"""
	
	def check_path(x, y, side) -> (int, int):
		# I hate a lot of if's but who cares if it's fast
		# Basically checks all indexes colliding with next path index
		if side == 'left':
			if field[y - 1][x] == 0 or field[y - 1][x - 1] == 0 or field[y][x - 1] == 0 or field[y + 1][x - 1] == 0 or \
					field[y + 1][x] == 0:
				return False
		elif side == 'right':
			if field[y - 1][x] == 0 or field[y + 1][x] == 0 or field[y + 1][x + 1] == 0 or field[y][x + 1] == 0 or \
					field[y - 1][x + 1] == 0:
				return False
		elif side == 'up':
			if field[y - 1][x] == 0 or field[y - 1][x - 1] == 0 or field[y][x - 1] == 0 or field[y][x + 1] == 0 or \
					field[y - 1][x + 1] == 0:
				return False
		elif side == 'down':
			if field[y][x - 1] == 0 or field[y + 1][x - 1] == 0 or field[y + 1][x] == 0 or field[y + 1][x + 1] == 0 or \
					field[y][x + 1] == 0:
				return False
		else:
			return False
		
		return True
	
	def generate_path(x, y, side):
		nonlocal field, next_gen
		
		if field[y][x] != 1 or not check_path(x, y, side):
			return
		
		field[y][x] = 0
		if field[y][x - 1] == 1 and (x - 1, y, 'left'):
			next_gen.append((x - 1, y, 'left'))
		if field[y][x + 1] == 1 and (x + 1, y, 'right'):
			next_gen.append((x + 1, y, 'right'))
		if field[y - 1][x] == 1 and (x, y - 1, 'up'):
			next_gen.append((x, y - 1, 'up'))
		if field[y + 1][x] == 1 and (x, y + 1, 'down'):
			next_gen.append((x, y + 1, 'down'))
	
	field = _get_starting_box(field_width, field_height)
	startX, startY = random.randint(1, field_width - 2), random.randint(1, field_height - 2)
	
	finishes = _get_random_exits(field_width, field_height, exits)
	
	field[startY][startX] = 0
	for endX, endY in finishes:
		field[endY][endX] = 3
	
	# Generation
	next_gen = [(startX, startY + 1, 'down'), (startX - 1, startY, 'left'),
	            (startX + 1, startY, 'right'), (startX, startY - 1, 'up')]
	while next_gen:
		last_index = len(next_gen) - 1  # It should delete random index at O(1) but somehow it's slower than O(n)
		random_index = random.randint(0, last_index)
		next_gen[random_index], next_gen[last_index] = next_gen[last_index], next_gen[random_index]
		generate_path(*next_gen.pop())
	
	for endX, endY in finishes:
		_gen_end(field, field_width, field_height, endX, endY, startX, startY)
	
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


def generate_field_custom(field_width: int, field_height: int, exits: int = 1,
                          weight_left: int = 1, weight_right: int = 1, weight_up: int = 1,
                          centered_spawn: bool = False, bfs: bool = False, random_node_chance: int = 0,
                          dead_end_chance: int = 0, guaranteed_generations: int = 10,
                          use_new_generator: bool = True,
                          consecutive_steps: int = 1, allow_half_steps: bool = False) -> (list, int, int):
	"""
	Customisable, slower than generate_field_original, but can have a lot of variety.
	4s for 1024x1024 (slower with random nodes - 6s)
	
	Weights are relative to where we are generating - if left is the highest weight, the labyrinth will steer to the left.
	
	:param exits: How many exits labyrinth has.
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
	:param use_new_generator: False - use old generator inside, it uses weights differently.
	:param consecutive_steps: When generating a tile, how many steps in that direction to do.
	:param allow_half_steps: When generating more than 1 step, convert walls to path, or not
	:return: A field, start X and Y.
	"""
	
	def check_path(x: int, y: int, side: int) -> (int, int):
		# Looks sad as hell, but who cares if it's fast
		# Basically checks all indexes colliding with next path x and y
		if side == 0:
			x -= 1
			if field[y][x] != 1:
				return
			elif field[y - 1][x] == 0 or field[y - 1][x - 1] == 0 or field[y][x - 1] == 0 or field[y + 1][x - 1] == 0 or \
					field[y + 1][x] == 0:
				return
		elif side == 2:
			x += 1
			if field[y][x] != 1:
				return
			elif field[y - 1][x] == 0 or field[y + 1][x] == 0 or field[y + 1][x + 1] == 0 or field[y][x + 1] == 0 or \
					field[y - 1][x + 1] == 0:
				return
		elif side == 1:
			y -= 1
			if field[y][x] != 1:
				return
			elif field[y - 1][x] == 0 or field[y - 1][x - 1] == 0 or field[y][x - 1] == 0 or field[y][x + 1] == 0 or \
					field[y - 1][x + 1] == 0:
				return
		elif side == 3:
			y += 1
			if field[y][x] != 1:
				return
			elif field[y][x - 1] == 0 or field[y + 1][x - 1] == 0 or field[y + 1][x] == 0 or field[y + 1][x + 1] == 0 or \
					field[y][x + 1] == 0:
				return
		else:
			return
		return x, y
	
	def generate_path_old(pointX, pointY, side):
		pathcords = check_path(pointX, pointY, side)
		
		if not pathcords:
			return
		pathX, pathY = pathcords
		field[pathY][pathX] = 0
		
		# left - 0, up - 1, right - 2, down - 3
		if side == 1:
			relative_sides = [2, 1, 0]
		elif side == 0:
			relative_sides = [1, 0, 3]
		elif side == 3:
			relative_sides = [0, 3, 2]
		else:
			relative_sides = [3, 2, 1]
		
		randomised_sides = []
		weights = [weight_right, weight_up, weight_left]
		for _ in range(3):
			index = random.choices(range(len(relative_sides)), weights, k=1)[0]
			randomised_sides.append(relative_sides[index])
			relative_sides.pop(index)
			weights.pop(index)
		
		next_gen.append((pathX, pathY, randomised_sides[2]))
		next_gen.append((pathX, pathY, randomised_sides[1]))
		next_gen.append((pathX, pathY, randomised_sides[0]))
	
	def generate_path_new(pointX, pointY, side, randomised_sides=None, steps_left=consecutive_steps) -> bool:
		if randomised_sides is None:  # Get new cords and check them
			if side == 1:
				relative_sides = [2, 1, 0]
			elif side == 0:
				relative_sides = [1, 0, 3]
			elif side == 3:
				relative_sides = [0, 3, 2]
			else:
				relative_sides = [3, 2, 1]
			# left - 0, up - 1, right - 2, down - 3
			
			randomised_sides = []  # From the least priority to most priority
			weights = [weight_right, weight_up, weight_left]
			for _ in range(3):
				index = random.choices(range(len(relative_sides)), weights, k=1)[0]
				randomised_sides.append(relative_sides[index])
				relative_sides.pop(index)
				weights.pop(index)
		
		while randomised_sides:
			rand_side = randomised_sides.pop()
			next_path_cords = check_path(pointX, pointY, rand_side)
			if not next_path_cords:
				continue
			next_x, next_y = next_path_cords
			
			if randomised_sides:  # If it is the starting step, save other sides
				next_gen.append((pointX, pointY, side, randomised_sides.copy()))
			
			if steps_left > 1:
				full_steps = generate_path_new(next_x, next_y, side, [rand_side], steps_left - 1)
				if allow_half_steps or full_steps:
					field[next_y][next_x] = 0
				return full_steps
			
			field[next_y][next_x] = 0
			next_gen.append((next_x, next_y, rand_side))
			return True
	
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
	# all sides are value coded:
	# left - 0, up - 1, right - 2, down - 3, same as indexes in field_checks
	next_gen = [(startX, startY, 0), (startX, startY, 1), (startX, startY, 2), (startX, startY, 3)]
	random.shuffle(next_gen)
	
	if bfs:
		priority_index = 0
	else:
		priority_index = -1
	
	if use_new_generator:
		path_generator = generate_path_new
	else:
		path_generator = generate_path_old
	
	_generation_cycle(next_gen, path_generator, priority_index, random_node_chance,
	                  dead_end_chance, guaranteed_generations)
	
	for endX, endY in finishes:
		_gen_end(field, field_width, field_height, endX, endY, startX, startY)
	
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


def generate_field_vector(field_width: int, field_height: int,
                          wall_width: int = 1, path_width: int = 1,
                          max_path_len: float = float("inf"), min_path_len: float = 1,
                          turn_angle_step: int = 30, ignore_tiles_radius: int = 3,
                          exits: int = 1, centered_spawn: bool = False, bfs: bool = False,
                          random_choice_chance: int = 0, dead_end_chance: int = 0, guaranteed_generations: int = 10,
                          reverse: bool = False) -> (list, int, int):
	"""
	Generates a maze by choosing a point, and shooting a path in a random direction.
	Very slow, but can look fun.
	16s for 256x256, but varies a lot
	:param wall_width: How many walls between paths at minimum.
	:param path_width: Makes paths wider.
	:param max_path_len: Makes generation less linear.
	:param min_path_len: Makes generation more blocky.
	:param turn_angle_step: Optimisation feature, if more, generator considers less angles for path generation.
	:param ignore_tiles_radius: When choosing a path, generator must ignore the closest tiles, otherwise it will
	consider itself as another path.
	:param exits: How many exits are there, will correct impossible values.
	:param centered_spawn: No random spawn location - always at a field center.
	:param bfs: True - BFS generation, False - DFS
	DFS generates faster, generates from last generated nodes, generally leads to 1 long path and few branches.
	BFS generates from first nodes, mostly creates same fields.
	:param random_choice_chance: What percentage of node generations should be chosen NOT on BFS or DFS but random.
	:param dead_end_chance: A chance to not generate a path.
	:param guaranteed_generations: How many generations will not roll a dead_end_chance.
	:param reverse: If true, it reverses  walls and paths.
	:return: A field, start X and Y.
	"""
	
	def check_angle(x, y, angle, ignore_tiles: set = None) -> bool:
		"""
		Changes inputted ignore_tiles
		:return: If there is another path in a radius of wall_width
		"""
		
		if ignore_tiles is None:
			ignore_tiles = set()
		
		ignore_tiles.add((round(x), round(y)))
		
		# We iterate over all angles clockwise in a circle, to check if there are already other paths
		# within wall_width, which would be too close
		for check_angle in range(angle - 90, angle + 90, check_angle_step):
			path = _generator_precise(x, y, check_angle, field_width, field_height, 1, 1,
			                          max_path_len=wall_width + path_width)
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
		for float_x, float_y in _generator_precise(check_x, check_y, angle, field_width, field_height, 0, 0,
		                                           max_path_len=min_path_len):
			if not check_angle(float_x, float_y, angle, ignore_tiles):
				continue
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
		for angle in range(0, 360, turn_angle_step):
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
		subpath_len = 0
		
		additional_tiles = {(0, 0)}
		if path_width > 1:
			for add_x, add_y in _generator_precise(start_x, start_y, chosen_angle + 90, field_width, field_height, 1, 1,
			                                       path_width // 2):
				additional_tiles.add((start_x - round(add_x), start_y - round(add_y)))
			for add_x, add_y in _generator_precise(start_x, start_y, chosen_angle - 90, field_width, field_height, 1, 1,
			                                       (path_width + 1) // 2):
				additional_tiles.add((start_x - round(add_x), start_y - round(add_y)))
		
		# Generating a path at chosen angle
		for float_x, float_y in _generator_precise(start_x, start_y, chosen_angle, field_width, field_height, 1, 1,
		                                           max_path_len=max_path_len):
			orig_x, orig_y = round(float_x), round(float_y)
			ignore_tiles_close.add((orig_x, orig_y))
			
			if check_angle(float_x, float_y, chosen_angle, ignore_tiles_close):
				break
			
			for add_x, add_y in additional_tiles:
				path_x, path_y = orig_x + add_x, orig_y + add_y
				new_ignore_tiles.add((path_x, path_y))
				ignore_tiles_close.add((path_x, path_y))
				
				if field[path_y][path_x] == 1:
					field[path_y][path_x] = 0
					if subpath_len > wall_width:  # It creates a new path every wall_width cuz it cannot be closer
						next_gen.append((path_x, path_y, new_ignore_tiles))
						subpath_len -= wall_width
			subpath_len += 1
	
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
	check_angle_step = int(360 / (wall_width + 1) / 20) + 1
	ignore_tiles_radius += wall_width  # Maybe I shouldn't do that, but it's annoying to change
	
	# Generation
	next_gen = []
	
	if bfs:
		priority_index = 0
	else:
		priority_index = -1
	generate_path(startX, startY)  # Calls first generation here because there is a chance to not generate later
	
	_generation_cycle(next_gen, generate_path, priority_index, random_choice_chance, dead_end_chance,
	                  guaranteed_generations)
	
	# After generation
	if reverse:
		# Walls will become paths, but these paths will not be connected, so I connect all walls in 1 new maze
		# connected_walls = []
		# for y, row in enumerate(field):
		# 	for x, tile in enumerate(row):
		# 		if tile == 1:
		# 			if connected_walls:
		# 				last_x, last_y = random.choice(connected_walls)
		# 				dest_x, dest_y = x, y
		# 				for dest_x, dest_y in _generator_between_points(last_x, last_y, x, y):
		# 					rx, ry = round(dest_x), round(dest_y)
		# 					path_tile = field[ry][rx]
		# 					if path_tile == 99:
		# 						last_x, last_y = rx, ry
		# 					elif path_tile == 1:
		# 						break
		#
		# 				dest_x, dest_y = round(dest_x), round(dest_y)
		# 				for step_x, step_y in _generator_between_points(last_x, last_y, dest_x, dest_y):
		# 					rx, ry = round(step_x), round(step_y)
		# 					if field[ry][rx] == 0:
		# 						field[ry][rx] = 99
		# 						connected_walls.append((rx, ry))
		#
		# 			this_room = set()
		# 			adjacent_walls = [(x, y)]
		# 			while adjacent_walls:
		# 				adjx, adjy = adjacent_walls.pop()
		# 				if field[adjy][adjx] == 1:
		# 					this_room.add((adjx, adjy))
		# 					field[adjy][adjx] = 99
		# 					adjacent_walls.extend(((x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)))
		# 			connected_walls.extend(this_room)
		# TODO: Yeah commenting code is bad, but now even debug is dying by itself, so nah, not finishing
		# but now, when you reverse, the mazes are impossible, oh no
		
		for y, row in enumerate(field):
			for x, tile in enumerate(row):
				if tile == 1:
					field[y][x] = 0
				elif tile == 0:
					field[y][x] = 1
	
	for endX, endY in finishes:
		_gen_end(field, field_width, field_height, endX, endY, startX, startY)
	
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


def generate_field_kruskal(field_width: int, field_height: int, exits: int = 1,
                           weight_left: int = 1, weight_right: int = 1, weight_up: int = 1,
                           centered_spawn: bool = False, bfs: bool = False, random_node_chance: int = 0,
                           dead_end_chance: int = 0, guaranteed_generations: int = 10,
                           use_new_generator: bool = True) -> (list, int, int):
	"""
	Customisable, slower than generate_field_original, but can have a lot of variety.
	4s for 1024x1024 (slower with random nodes - 6s)

	Weights are relative to where we are generating - if left is the highest weight, the labyrinth will steer to the left.

	:param exits: How many exits labyrinth has.
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
	:param use_new_generator: False - use old generator inside, it uses weights differently.
	:return: A field, start X and Y.
	"""
	
	def check_path(x: int, y: int, side: int) -> (int, int):
		# Looks sad as hell, but who cares if it's fast
		# Basically checks all indexes colliding with next path x and y
		if side == 0:
			x -= 1
			if field[y][x] != 1:
				return
			elif field[y - 1][x] == 0 or field[y - 1][x - 1] == 0 or field[y][x - 1] == 0 or field[y + 1][x - 1] == 0 or \
					field[y + 1][x] == 0:
				return
		elif side == 2:
			x += 1
			if field[y][x] != 1:
				return
			elif field[y - 1][x] == 0 or field[y + 1][x] == 0 or field[y + 1][x + 1] == 0 or field[y][x + 1] == 0 or \
					field[y - 1][x + 1] == 0:
				return
		elif side == 1:
			y -= 1
			if field[y][x] != 1:
				return
			elif field[y - 1][x] == 0 or field[y - 1][x - 1] == 0 or field[y][x - 1] == 0 or field[y][x + 1] == 0 or \
					field[y - 1][x + 1] == 0:
				return
		elif side == 3:
			y += 1
			if field[y][x] != 1:
				return
			elif field[y][x - 1] == 0 or field[y + 1][x - 1] == 0 or field[y + 1][x] == 0 or field[y + 1][x + 1] == 0 or \
					field[y][x + 1] == 0:
				return
		else:
			return
		return x, y
	
	def generate_path_old(pointX, pointY, side):
		pathcords = check_path(pointX, pointY, side)
		
		if not pathcords:
			return
		pathX, pathY = pathcords
		field[pathY][pathX] = 0
		
		# left - 0, up - 1, right - 2, down - 3
		if side == 1:
			relative_sides = [2, 1, 0]
		elif side == 0:
			relative_sides = [1, 0, 3]
		elif side == 3:
			relative_sides = [0, 3, 2]
		else:
			relative_sides = [3, 2, 1]
		
		randomised_sides = []
		weights = [weight_right, weight_up, weight_left]
		for _ in range(3):
			index = random.choices(range(len(relative_sides)), weights, k=1)[0]
			randomised_sides.append(relative_sides[index])
			relative_sides.pop(index)
			weights.pop(index)
		
		next_gen.append((pathX, pathY, randomised_sides[2]))
		next_gen.append((pathX, pathY, randomised_sides[1]))
		next_gen.append((pathX, pathY, randomised_sides[0]))
	
	def generate_path_new(pointX, pointY, side, randomised_sides=None):
		if randomised_sides is None:  # Get new cords and check them
			if side == 1:
				relative_sides = [2, 1, 0]
			elif side == 0:
				relative_sides = [1, 0, 3]
			elif side == 3:
				relative_sides = [0, 3, 2]
			else:
				relative_sides = [3, 2, 1]
			# left - 0, up - 1, right - 2, down - 3
			
			randomised_sides = []  # From the least priority to most priority
			weights = [weight_right, weight_up, weight_left]
			for _ in range(3):
				index = random.choices(range(len(relative_sides)), weights, k=1)[0]
				randomised_sides.append(relative_sides[index])
				relative_sides.pop(index)
				weights.pop(index)
		
		while randomised_sides:
			rand_side = randomised_sides.pop()
			next_path_cords = check_path(pointX, pointY, rand_side)
			if not next_path_cords:
				continue
			next_x, next_y = next_path_cords
			field[next_y][next_x] = 0
			
			next_gen.append((pointX, pointY, side, randomised_sides))
			next_gen.append((next_x, next_y, rand_side))
			return
	
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
	# all sides are value coded:
	# left - 0, up - 1, right - 2, down - 3, same as indexes in field_checks
	next_gen = [(startX, startY, 0), (startX, startY, 1), (startX, startY, 2), (startX, startY, 3)]
	random.shuffle(next_gen)
	
	if bfs:
		priority_index = 0
	else:
		priority_index = -1
	
	if use_new_generator:
		path_generator = generate_path_new
	else:
		path_generator = generate_path_old
	
	_generation_cycle(next_gen, path_generator, priority_index, random_node_chance,
	                  dead_end_chance, guaranteed_generations)
	
	for endX, endY in finishes:
		_gen_end(field, field_width, field_height, endX, endY, startX, startY)
	
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


if __name__ == '__main__':
	import time
	
	random.seed(213498790134278)
	
	tries = 10
	size = 2 ** 2
	while size <= 2 ** 7:
		width = height = size
		times = []
		for _ in range(tries):
			s = time.time()
			generate_field_custom(size, size)
			s = time.time() - s
			times.append(s)
		
		print(size, times)
		print(min(times), sum(times) / len(times), max(times))
		print()
		size *= 2
