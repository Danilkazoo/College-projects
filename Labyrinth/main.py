import pygame
from pygame.locals import (
	K_w, K_s, K_a, K_d,
	K_ESCAPE, QUIT,
	K_LEFT, K_RIGHT, K_UP, K_DOWN)

import generators


def start_game(field_width, field_height, block_size, exits):
	def minmax(num, min, max):
		if num < min:
			return min
		if num > max:
			return max
		return num
	
	class Player(pygame.sprite.Sprite):
		def __init__(self, size, spawn_x, spawn_y, player_color):
			super(Player, self).__init__()
			self.surf = pygame.Surface((size, size))
			self.surf.fill(player_color)
			self.rect = self.surf.get_rect()
			self.X = spawn_x
			self.Y = spawn_y
			self.size = size
		
		def check_move(self, X, Y):
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
			
			if self.check_move(newX, oldY):
				self.X = newX
			if self.check_move(self.X, newY):
				self.Y = newY
			
			return oldX, oldY
	
	def win():
		nonlocal screen, running, world
		img = pygame.image.load(r"603e0413c81f611898488e6c2f736864.jpeg").convert()
		width, height = img.get_size()
		screen = pygame.display.set_mode((width, height))
		world.set_alpha(0)
		
		screen.blit(img, (0, 0))
		pygame.display.flip()
		
		while True:
			pressed_keys = pygame.key.get_pressed()
			for event in pygame.event.get():
				if event.type == QUIT:
					return
			
			if pressed_keys[K_ESCAPE]:
				return
	
	def calc_camera(player, block_size, camera_width, camera_height):
		cameraX = (player.X * block_size) - (camera_width * block_size / 2)
		cameraY = (player.Y * block_size) - (camera_height * block_size / 2)
		
		cameraX = minmax(cameraX, 0, max_cam_x)
		cameraY = minmax(cameraY, 0, max_cam_y + block_size)
		
		return -cameraX, -cameraY
	
	def display_lab(screen, world, old_X, old_Y, camera_pos):
		pygame.draw.rect(world, (255, 255, 255),
		                 pygame.Rect(old_X * block_size, old_Y * block_size, block_size, block_size))
		world.blit(player.surf, (player.X * block_size, player.Y * block_size))
		
		screen.blit(world, camera_pos)
		pygame.display.flip()
	
	pygame.init()
	pygame.display.set_caption("AAAAAAAA")
	screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
	
	# field, spawn_x, spawn_y = generators.generate_field_chaos(field_width, field_height, wall_width=1, path_width=1,
	#                                                           min_path_len=5, check_angle_step=15, max_path_len=15,
	#                                                           centered_spawn=False, random_choice_chance=100,
	#                                                           guaranteed_generations=50, dead_end_chance=50)
	field, spawn_x, spawn_y = generators.generate_field_custom(field_width, field_height, random_node_chance=40, dead_end_chance=100)
	
	# In short, you choose a camera height, but it will be changed if it does not the screen height
	camera_width, camera_height = 10000, 10000
	window_width = minmax(camera_width * block_size, 100, screen_width - 100)
	window_height = minmax(camera_height * block_size, 100, screen_height - 100)
	camera_width = minmax(camera_width, 1, window_width // block_size)
	camera_height = minmax(camera_height, 1, window_height // block_size)
	
	if camera_width > field_width:
		if camera_width * block_size > window_width:
			max_cam_x = (field_width * block_size) - window_width
		else:
			max_cam_x = 0
	else:
		max_cam_x = (field_width - camera_width) * block_size
	if camera_height > field_height:
		if camera_height * block_size > window_height:
			max_cam_y = (field_height * block_size) - window_height
		else:
			max_cam_y = 0
	else:
		max_cam_y = (field_height - camera_height) * block_size
	
	player_color = (255, 0, 0)
	bg_color = (255, 255, 255)
	wall_color = (0, 0, 0)
	exit_color = (150, 150, 255)
	
	screen = pygame.display.set_mode((window_width, window_height))
	screen.fill(wall_color)
	
	world = pygame.Surface((len(field[0]) * block_size, len(field) * block_size))
	world.fill(bg_color)
	
	player = Player(block_size, spawn_x, spawn_y, player_color)
	world.blit(player.surf, (player.X * block_size, player.Y * block_size))
	
	clock = pygame.time.Clock()
	
	# Draw the labyrinth
	for y, row in enumerate(field):
		for x, cell in enumerate(row):
			if cell == 1:
				pygame.draw.rect(world, wall_color, pygame.Rect(x * block_size, y * block_size, block_size, block_size))
			elif cell == 2:
				pygame.draw.rect(world, exit_color, pygame.Rect(x * block_size, y * block_size, block_size, block_size))
	
	camera_pos = calc_camera(player, block_size, camera_width, camera_height)
	screen.blit(world, camera_pos)
	pygame.display.flip()
	
	last_move_tick = 0
	move_delay = 10  # in ticks (120 per second)
	
	running = True
	while running:
		pressed_keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
				break
		
		if pressed_keys[K_ESCAPE]:
			break
		
		if any(pressed_keys) and last_move_tick > move_delay:
			if last_move_tick > move_delay:
				oldX, oldY = player.move(pressed_keys)
				if player.X == oldX and player.Y == oldY:
					continue
				
				if field[player.Y][player.X] == 2:
					win()
					break
				
				camera_pos = calc_camera(player, block_size, camera_width, camera_height)
				display_lab(screen, world, oldX, oldY, camera_pos)
				last_move_tick = -1
		
		last_move_tick += 1
		clock.tick(120)
	
	pygame.quit()


if __name__ == '__main__':
	import time
	
	test_sizes = (
		(5, 5, 50, 1), (10, 10, 50, 1), (20, 20, 50, 1), (50, 50, 20, 1), (100, 100, 10, 1), (500, 500, 5, 5),
		(1000, 1000, 3, 20), (1000, 1000, 2, 20), (1000, 1000, 1, 20),
		(100, 5, 20, 3), (100, 10, 20, 3), (5, 100, 20, 3), (10, 100, 20, 3), (20, 1000, 5, 10), (1000, 20, 2, 10))
	
	for width, height, tile_size, ends in test_sizes:
		print(f"\nLabyrinth {width = } {height = } {tile_size = } {ends = }")
		start = time.time()
		start_game(width, height, tile_size, ends)
		print("Speedrun time - ", time.time() - start)

# анимация генерации
# можно конечно по фану добавить выбор сложности / разные уровни, где игра постепенно становится сложнее
# может ещё и добавить бафы / дебафы во время игры, по типу размера камеры, или временного бафа на фулл карту камеру
# в теории можно даже делать zoom in эффект, тупо увеличивая размер квадратов ? игра всё равно должна показывать игрока
# хотя тогда надо оставлять игрока нормально относительно от камеры
# фикс камеры, которая изначально лаганная (может тупо обновлять в первом кадре)
# скорость передвижения и delay между шагами должен быть в классе игрока
# просто для угара пусть будет генериться лабиринт, потом его копируешь в 4 ровные копии (или отзеркаленные), и туда копируешь игрока, ну и пусть будет всё видно
# сглаживание камеры ?
# ну и уже известные алгоритмы генерации тоже реализовать весело

# менюшка с разными лабиринтами, у каждого - его название, и превью, хачу по фану генерить превьюшки
# ну и где-то снизу может быть мега стори режим значт, где и могут быть апгрейды всякие, можно даже пару предметов сделать типа ломания стен вокруг себя
# в теории при наводке мышью превью можно увеличить тупо увеличив размер клеток в нём, над таким эффектом надо поработать

# кстати об этом - да, после анимации генерации лабиринта сделай анимацию приближения или отдаления к персу, чтобы сразу понимать где я и кто я
# а вот как нормально эту анимацию сделать - вопрос, типа надо отдалять от перса просто чтобы чётко знать где он

# звучит как угарная идея сделать перса двигающимся не по матрице, а просто по полю пайгейма, и генерить лабиринт чисто на поле, проверяя коллизии
# шутка в том что я же так могу генерить лабиринт тупо рандомными линиями, просто выбираешь рандомный угол, и туда генеришь лабиринт
# важно только чтобы перс смог пройти в любую точку лабиринта
# (такое можно сделать тупо создавая лабиринт разрешением в экран, где каждая стена - пиксель, перс может двигаться также...)
# но для такого огромного лабиринта надо бы придумать более эффективный алгоритм, а то будет реальная жесть с генерацией в 5 часов
# в общем, выбираешь рандомную сторону - рисуешь туда стену, она заканчивается либо когда достигает опр. длинны, либо доходит до другой стены
# ну и наверное надо генерить стены не из прям каждого пикселя, лол, а ограничивая их расстоянием от других стен чтобы игрок мог пройти
# так и генерация будет быстрее

# если шизануться, то можно создавать лабиринт с кучей уровней, в рандомных тупиках создавая переход на другой уровень на тех же кордаъ
# и, на каждом уровне делая то же самое. По факту получится 3-х мерный лабиринт, удачи такой пройти, лел... но, звучит как угарная идея
# особенно для троллинга с лабиринтом в 100 уровней

# куча инфы https://habr.com/ru/articles/445378/
