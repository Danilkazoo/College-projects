import random
import time


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


def generate_field_original_optimised(field_width: int, field_height: int, exits: int = 1) -> (list, int, int):
	"""
	More blocky generation, has a lot of strange 1 block paths, kinda easy to predict on small sizes.
	O(n^2), 4.9s for 1024x1024
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
	
	def gen_end(endX, endY):
		nonlocal field
		
		if endX == 0:
			move = (1, 0)
			to_mine = field_height - 2
		elif endX == field_height - 1:
			move = (-1, 0)
			to_mine = field_height - 2
		elif endY == 0:
			move = (0, 1)
			to_mine = field_width - 2
		else:
			move = (0, -1)
			to_mine = field_width - 2
		
		for _ in range(to_mine):
			endX += move[0]
			endY += move[1]
			field[endY][endX] = 0
			
			if field[endY][endX] == 0 or field[endY + move[0]][endX + move[1]] == 0 or field[endY - move[0]][
				endX - move[1]] == 0:
				return
	
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
		gen_end(endX, endY)
	
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
	O(n^2), but very random, so the bigger the input - the longer it takes, realistically O(n^3). 40s for 1024x1024
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
	
	def gen_end(endX, endY):
		nonlocal field
		
		if endX == 0:
			move = (1, 0)
			to_mine = fieldY - 2
		elif endX == fieldY - 1:
			move = (-1, 0)
			to_mine = fieldY - 2
		elif endY == 0:
			move = (0, 1)
			to_mine = fieldX - 2
		else:
			move = (0, -1)
			to_mine = fieldX - 2
		
		for _ in range(to_mine):
			endX += move[0]
			endY += move[1]
			field[endY][endX] = 0
			
			if field[endY][endX] == 0 or field[endY + move[0]][endX + move[1]] == 0 or field[endY - move[0]][
				endX - move[1]] == 0:
				return
	
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
		gen_end(endX, endY)
	
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
                          centered_spawn: bool = False,
                          bfs: bool = False, randomised_node_percentage: int = 0) -> (list, int, int):
	"""
	Customisable, slower than generate_field_original_optimised, but can have a lot of variety.
	O(n^2), 5.5s for 1024x1024
	
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
	:param randomised_node_percentage: What percentage of node generations should be chosen NOT on BFS or DFS but random.
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
	
	def gen_end(endX, endY):
		nonlocal field
		
		if endX == 0:
			move = (1, 0)
			to_mine = field_height - 2
		elif endX == field_height - 1:
			move = (-1, 0)
			to_mine = field_height - 2
		elif endY == 0:
			move = (0, 1)
			to_mine = field_width - 2
		else:
			move = (0, -1)
			to_mine = field_width - 2
		
		for _ in range(to_mine):
			endX += move[0]
			endY += move[1]
			field[endY][endX] = 0
			
			if field[endY][endX] == 0 or field[endY + move[0]][endX + move[1]] == 0 or field[endY - move[0]][
				endX - move[1]] == 0:
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
	next_gen = [lambda: generate_path(startX, startY, 'left'), lambda: generate_path(startX, startY, 'up'),
	            lambda: generate_path(startX, startY, 'right'), lambda: generate_path(startX, startY, 'down')]
	
	if bfs:
		priority_index = 0
	else:
		priority_index = -1
	
	# Two cycles for optimisation
	if randomised_node_percentage:
		while next_gen:
			if random.randint(1, 100) <= randomised_node_percentage:
				generate_index = random.randint(0, len(next_gen) - 1)
			else:
				generate_index = priority_index
			
			next_gen.pop(generate_index)()
	else:
		generate_index = priority_index
		while next_gen:
			next_gen.pop(generate_index)()
	
	for endX, endY in finishes:
		gen_end(endX, endY)
	
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
		                             randomised_node_percentage=random_node_percentage)
	else:
		return generate_field_custom(field_width, field_height, exits, centered_spawn=centered_spawn,
		                             weight_up=forward_strength, weight_left=steer_strength, weight_right=100,
		                             randomised_node_percentage=random_node_percentage)


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
		                             weight_up=100, weight_right=1, weight_left=1, randomised_node_percentage=10)
	else:
		return generate_field_custom(field_width, field_height, exits, centered_spawn=False,
		                             weight_up=100, weight_left=1, weight_right=1, randomised_node_percentage=10)


def generate_corridors_small(field_width: int, field_height: int, exits: int = 1):
	"""Specific configuration of weighted generation, labyrinth will look like a defined spiral with long corridors."""
	if random.randint(0, 1):
		return generate_field_custom(field_width, field_height, exits, centered_spawn=False,
		                             weight_up=100, weight_right=1, weight_left=1, randomised_node_percentage=40)
	else:
		return generate_field_custom(field_width, field_height, exits, centered_spawn=False,
		                             weight_up=100, weight_left=1, weight_right=1, randomised_node_percentage=40)


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
	                             randomised_node_percentage=random_node_percentage)


if __name__ == '__main__':
	tries = 1
	
	size = 4
	while size < 1000:
		size *= 2
		width = height = size
		times = []
		for _ in range(tries):
			s = time.time()
			generate_field_custom(width, height)
			times.append(time.time() - s)
		
		print(size, times)
		print(sum(times) / len(times))
		print()
