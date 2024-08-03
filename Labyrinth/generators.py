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
	for _ in range(exits):
		random_finish = random.randint(0, len(possible_cords) - 1)
		
		finishes.add(possible_cords.pop(random_finish))
	
	return finishes


def generate_field_1(field_width: int, field_height: int, exits: int = 1) -> (list, int, int):
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


if __name__ == '__main__':
	tries = 1
	
	size = 4
	while size < 1000:
		size *= 2
		width = height = size
		times = []
		for _ in range(tries):
			s = time.time()
			generate_field_original(width, height)
			times.append(time.time() - s)
		
		print(size, times)
		print(sum(times) / len(times))
		print()
