import pygame
import random
from pygame.locals import (
	K_w, K_s, K_a, K_d,
	K_ESCAPE, QUIT,
	K_LEFT, K_RIGHT, K_UP, K_DOWN)


def minmax(num, min, max):
	if num < min:
		return min
	if num > max:
		return max
	return num


def generate_field(fieldY, fieldX, finishes=1):
	field = []
	for y in range(fieldY):
		field.append([2])
		for x in range(fieldX - 2):
			if y == 0 or y == fieldY - 1:
				field[y].append(2)
			else:
				field[y].append(1)
		field[y].append(2)
	
	# Random start and finish
	startX, startY = random.randint(1, fieldX - 2), random.randint(1, fieldY - 2)
	if random.randint(0, 1):
		endX, endY = random.choice((0, fieldX - 1)), random.randint(1, fieldY - 2)
	else:
		endX, endY = random.choice((0, fieldX - 2)), random.randint(1, fieldY - 2)
	
	# ШАНСЫ МОЖНО УДАЛИТЬ, ОНИ ЭКСПЕРИМЕНТ, Я ИГРАЮ В НОТЧА
	def generate_path(pointX, pointY, destX, destY, *sides, pathlen=1):
		nonlocal field, next_gen
		possible_paths = []
		if 'left' in sides or 'all' in sides:
			possible_paths.append([pointX - 1, pointY, 'left'])
		if 'right' in sides or 'all' in sides:
			possible_paths.append([pointX + 1, pointY, 'right'])
		if 'up' in sides or 'all' in sides:
			possible_paths.append([pointX, pointY + 1, 'up'])
		if 'down' in sides or 'all' in sides:
			possible_paths.append([pointX, pointY - 1, 'down'])
		
		# Checks
		i = 0
		while i < len(possible_paths):
			pathX, pathY, side = possible_paths[i]
			
			# Убираю все углы и уже пустые места
			if field[pathY][pathX] == 0 or field[pathY][pathX] == 2:
				possible_paths.pop(i)
				continue
			
			close_walls = []
			if side == 'left':
				close_walls.append(field[pathY][pathX - 1])
				close_walls.append(field[pathY + 1][pathX - 1])
				close_walls.append(field[pathY - 1][pathX - 1])
				close_walls.append(field[pathY + 1][pathX])
				close_walls.append(field[pathY - 1][pathX])
			if side == 'right':
				close_walls.append(field[pathY][pathX + 1])
				close_walls.append(field[pathY + 1][pathX + 1])
				close_walls.append(field[pathY - 1][pathX + 1])
				close_walls.append(field[pathY + 1][pathX])
				close_walls.append(field[pathY - 1][pathX])
			if side == 'up':
				close_walls.append(field[pathY + 1][pathX - 1])
				close_walls.append(field[pathY + 1][pathX + 1])
				close_walls.append(field[pathY + 1][pathX])
				close_walls.append(field[pathY][pathX + 1])
				close_walls.append(field[pathY][pathX - 1])
			if side == 'down':
				close_walls.append(field[pathY - 1][pathX - 1])
				close_walls.append(field[pathY - 1][pathX + 1])
				close_walls.append(field[pathY - 1][pathX])
				close_walls.append(field[pathY][pathX + 1])
				close_walls.append(field[pathY][pathX - 1])
			
			if not all(close_walls):
				possible_paths.pop(i)
				continue
			
			i += 1
		
		# Если тупик - тупик
		if not possible_paths:
			return
		
		# Так оно будет рандомным, иначе пути получаются прямыми
		random.shuffle(possible_paths)
		
		for pathX, pathY, l in possible_paths:
			field[pathY][pathX] = 0
			next_gen.insert(0, f"generate_path({pathX}, {pathY}, {destX}, {destY}, 'all', pathlen={pathlen + 1})")
			break
		next_gen.insert(0, f"generate_path({pointX}, {pointY}, {destX}, {destY}, 'all', pathlen={pathlen})")
		
		'''for pathX, pathY, l in possible_paths:
			field[pathY][pathX] = 0
			generate_path(pathX, pathY, destX, destY, 'all', pathlen=pathlen + 1)'''
	
	def gen_end(endX, endY):
		nonlocal field
		
		if endX == 0:
			side = 'left'
		elif endX == fieldX - 1:
			side = 'right'
		elif endY == 0:
			side = 'down'
		else:
			side = 'up'
		
		mined = list((endX, endY))
		
		while True:
			if side == 'left':
				mined[0] += 1
			elif side == 'right':
				mined[0] -= 1
			elif side == 'up':
				mined[1] -= 1
			else:
				mined[1] += 1
			
			if field[mined[1]][mined[0]] == 0:
				return
			else:
				field[mined[1]][mined[0]] = 0
	
	field[startY][startX] = 0
	field[endY][endX] = 0
	
	next_gen = ["generate_path(startX, startY, endX, endY, 'all')"]
	i = 0
	ten_percent = fieldY * fieldX // 10
	
	while next_gen:
		exec(next_gen[0])
		next_gen.pop(0)
		# Если менять рандом, то в теории будет творится бОльший хаос
		if len(next_gen) < 2000:
			if random.randint(1, 20) == 1:
				random.shuffle(next_gen)
		i += 1
		if i % ten_percent == 0:
			print(i)
	
	gen_end(endX, endY)
	
	# Just for return
	for y in range(fieldY):
		field[y][0] = 1
		field[y][fieldX - 1] = 1
	for x in range(fieldX):
		field[0][x] = 1
		field[fieldY - 1][x] = 1
	field[endY][endX] = 2
	
	return field, startX, startY


class Player(pygame.sprite.Sprite):
	def __init__(self, size, px, py):
		super(Player, self).__init__()
		self.surf = pygame.Surface((size, size))
		self.surf.fill((255, 0, 0))
		self.rect = self.surf.get_rect()
		self.X = px
		self.Y = py
	
	def check(self, X, Y):
		global field, fieldX, fieldY
		
		if field[Y][X] == 2:
			global win
			win()
			return True
		
		if field[Y][X] == 1:
			return False
		return True
	
	def move(self, pressed_keys):
		oldX, oldY = self.X, self.Y
		newX, newY = self.X, self.Y
		if pressed_keys[K_w] or pressed_keys[K_UP]:
			newY -= 1
		if pressed_keys[K_s] or pressed_keys[K_DOWN]:
			newY += 1
		if pressed_keys[K_d] or pressed_keys[K_RIGHT]:
			newX += 1
		if pressed_keys[K_a] or pressed_keys[K_LEFT]:
			newX -= 1
		
		if self.check(newX, newY):
			self.X, self.Y = newX, newY
		return oldX, oldY


def win():
	global screen, daenda, running, world
	imp = pygame.image.load(r"603e0413c81f611898488e6c2f736864.jpeg").convert()
	width, height = imp.get_size()
	screen = pygame.display.set_mode((width, height))
	world.set_alpha(0)
	
	screen.blit(imp, (0, 0))
	daenda = True
	running = False


def calc_camera(pX, pY, square_size, camera_size):
	cameraX = pX * square_size - camera_size * square_size
	cameraY = pY * square_size - camera_size * square_size
	
	if cameraX < 0:
		cameraX = 0
	if cameraY < 0:
		cameraY = 0
	
	return -cameraX, -cameraY


# Теперь игрок не спавнится как надо, я должен это пофиксить, это после ограничения шафла
def display_lab(screen, world, old_X, old_Y):
	pygame.draw.rect(world, (255, 255, 255),
	                 pygame.Rect(old_X * block_size, old_Y * block_size, block_size, block_size))
	world.blit(PP.surf, (PP.X * block_size, PP.Y * block_size))
	
	screen.blit(world, camera_pos)
	pygame.display.flip()


fieldY, fieldX = 20, 20
field, px, py = generate_field(fieldY, fieldX)
print('Field generated')

pygame.init()
wX, wY = pygame.display.get_desktop_sizes()[0]
block_size = 20
camera_size = 10
screen = pygame.display.set_mode(
	(minmax(camera_size * block_size * 3, 100, wX - 100), minmax(camera_size * block_size * 3, 100, wY - 100)),
	pygame.RESIZABLE)
pygame.display.set_caption("AAAAAAAA")
clock = pygame.time.Clock()

PP = Player(block_size, px, py)
move_ticks = 0
move_delay = 10
wanna_move = False
last_move = ...

running = True
daenda = False
camera_pos = calc_camera(PP.X, PP.Y, block_size, camera_size)

world = pygame.Surface((len(field[0]) * block_size, len(field) * block_size))
screen.fill((0, 0, 0))
world.fill((255, 255, 255))

todraw = []
for y, row in enumerate(field):
	for x, cell in enumerate(row):
		if cell == 1:
			todraw.append((pygame.Rect(x * block_size, y * block_size, block_size, block_size), (0, 0, 0)))
		elif cell == 2:
			todraw.append((pygame.Rect(x * block_size, y * block_size, block_size, block_size), (150, 150, 255)))

world.blit(PP.surf, (PP.X * block_size, PP.Y * block_size))
for sq in todraw:
	pygame.draw.rect(world, sq[1], sq[0])

screen.blit(world, camera_pos)
pygame.display.flip()
while running:
	pressed_keys = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False
	
	if pressed_keys[K_ESCAPE]:
		running = False
	
	if any(pressed_keys) and move_ticks > move_delay:
		wanna_move = True
		last_move = pressed_keys
	
	# Мы тут двигаемся йопта
	if wanna_move:
		if move_ticks > move_delay:
			oldX, oldY = PP.move(last_move)
			move_ticks = 0
			wanna_move = False
			camera_pos = calc_camera(PP.X, PP.Y, block_size, camera_size)
			
			display_lab(screen, world, oldX, oldY)
	
	move_ticks += 1
	clock.tick(120)

running = True
while running:
	pressed_keys = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False
	
	if pressed_keys[K_ESCAPE]:
		running = False

pygame.quit()

# Надо добавить разветвления, тогда можно добавить максимальную длинну пути - тогда я смогу отдельно создавать фейки ака "maxlen = 10", и длинна этого фейка будет не больше 10
# Либо не надо, потому что пока я убирал гигантские рекурсии дабы сделать гигантский лабиринт, я почти случайно добавил хорошую генерацию...
# С гигантскими лабиринтами надо делать как сделал миша, так тупо эффективней
# Ешё пусть он запоминает когда кадр обновлялся а когда нет, и рисует только когда кадр новый
# И, обновляет он не всю карту - а лишь картинку игрока
# Может быть стоит функции заменить на сет, тогда надо проверить рандом шафл с сетами
# Улучшить алгоритм свой и проверить другие, их скорость, добавить длинные корридоры по фану
# Например не перемешивать, а просто выбирать рандомную функцию из списка

# Иногда лабиринт закрывает доступ к выходу... хотя по логике такого быть не должно
# Игрок вроде всегда спавнится, но камера иногда за ним тупо не следует...

# Разные алгоритмы, их скорость, и, оптимизация моего алгоритма - на потом, гы
