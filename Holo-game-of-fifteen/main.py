import random
import pygame

pygame.init()
pygame.display.set_caption('Holo is top')

# Customise here
imagename = "Example_Image.jpg"  # Just add a file and change this variable

# HOW MANY CUTS (we have a great knife)
# The size of the field (default 4x4) (doesn't work properly with unequal sides)
Board_Width = Board_Height = 10
tile_size = 200
offset_coef = 0.05  # Offset between tiles will be size * coefficient
border_size = 20

tile_offset = int(tile_size * offset_coef)
total_board_width = tile_size * Board_Width + tile_offset * (Board_Width - 1) + border_size * 2
total_board_height = tile_size * Board_Height + tile_offset * (Board_Height - 1) + border_size * 2

window_width = min(pygame.display.Info().current_w - 50, total_board_width)
window_height = min(pygame.display.Info().current_h - 50, total_board_height)

# This look awful, but in short, it resizes tiles to fit in the screen
if total_board_width > window_width:
	tile_size = (window_width - border_size * 2) // ((1 + offset_coef) * Board_Width)
	tile_offset = tile_size * offset_coef
	total_board_width = tile_size * Board_Width + tile_offset * (Board_Width - 1) + border_size * 2
	total_board_height = tile_size * Board_Height + tile_offset * (Board_Height - 1) + border_size * 2
if total_board_height > window_height:
	tile_size = (window_height - border_size * 2) // ((1 + offset_coef) * Board_Height)
	tile_offset = tile_size * offset_coef
	total_board_width = tile_size * Board_Width + tile_offset * (Board_Width - 1) + border_size * 2
	total_board_height = tile_size * Board_Height + tile_offset * (Board_Height - 1) + border_size * 2

window_width, window_height = total_board_width, total_board_height
image_width = total_board_width - border_size * 2 - tile_offset * (Board_Width - 1)
image_height = total_board_height - border_size * 2 - tile_offset * (Board_Height - 1)
Window = pygame.display.set_mode((window_width, window_height))
IMAGE = pygame.image.load(imagename).convert_alpha()
IMAGE = pygame.transform.smoothscale(IMAGE, (image_width, image_height))


def GenerateBoard():
	def inversions(arr):
		inv = 0
		for i in range(len(arr)):
			while arr[i] != i:
				inv += 1
				temp = arr[i]
				arr[i] = arr[temp]
				arr[temp] = temp
		return inv
	
	def snake_arr(arr):
		snake_arr = []
		for i in range(Board_Height):
			if i % 2 == 0:
				for j in range(Board_Width):
					snake_arr.append(arr[i * Board_Width + j])
			else:
				for j in range(Board_Width - 1, -1, -1):
					snake_arr.append(arr[i * Board_Width + j])
		
		return snake_arr
	
	RandomNumbers = list(range(1, (Board_Width * Board_Height)))
	RandomNumbers.append(0)
	
	start_inversions = inversions(snake_arr(RandomNumbers))
	
	random.shuffle(RandomNumbers)
	empty_index = RandomNumbers.index(0)
	RandomNumbers[empty_index], RandomNumbers[Board_Width * Board_Height - 1] = RandomNumbers[
		Board_Width * Board_Height - 1], RandomNumbers[empty_index]
	
	goal_inversions = inversions(snake_arr(RandomNumbers))
	
	RandomNumbers[Board_Width * Board_Height - 1] = "☢"
	
	if start_inversions % 2 != goal_inversions % 2:
		RandomNumbers[0], RandomNumbers[1] = RandomNumbers[1], RandomNumbers[0]
	
	return [[RandomNumbers[j + i * Board_Height] for j in range(Board_Height)] for i in range(Board_Width)]  # matrix


# check for win (we never won)
def check(field):
	for i in range(Board_Width):
		for j in range(Board_Height):
			if field[i][j] != (i * Board_Height) + j + 1:
				if i == Board_Width - 1 and j == Board_Height - 1:
					return True
				return False
	return True


def CreateSquare(x, y, Window, i, Size):
	Image_X = (i % Board_Width) * Size
	Image_Y = (i // Board_Height) * Size
	
	Window.blit(IMAGE, (x, y), (Image_X, Image_Y, Size, Size))


def out(arr):
	global Window
	
	pygame.draw.rect(Window, (0, 0, 0), pygame.Rect(0, 0, window_width, window_height))  # Black square on entire screen
	
	for i in range(len(arr)):
		for j in range(len(arr[0])):
			if arr[i][j] != "☢":
				CreateSquare(x=j * tile_size + j * tile_offset + border_size,
				             y=i * tile_size + i * tile_offset + border_size,
				             Window=Window, i=arr[i][j] - 1, Size=tile_size)
	pygame.display.update()


# Moevement by Y is inversed
def move(field, move):
	global move_speed, last_move_tick, instant_move, move_lock
	
	if not instant_move and last_move_tick < move_speed:
		return
	if move_lock:
		return
	
	for i in range(Board_Width):
		for j in range(Board_Height):
			if "☢" == field[i][j]:
				y, x = i, j
	
	if move == "Left":
		if x <= 0:
			return
		field[y][x - 1], field[y][x] = field[y][x], field[y][x - 1]
	elif move == "Right":
		if x >= Board_Width - 1:
			return
		field[y][x + 1], field[y][x] = field[y][x], field[y][x + 1]
	elif move == "Up":
		if y <= 0:
			return
		field[y - 1][x], field[y][x] = field[y][x], field[y - 1][x]
	elif move == "Down":
		if y >= Board_Height - 1:
			return
		field[y + 1][x], field[y][x] = field[y][x], field[y + 1][x]
	
	if check(field):
		global Window
		
		print("YOU WON")
		
		IMAGE = pygame.image.load(imagename).convert_alpha()
		IMAGE = pygame.transform.smoothscale(IMAGE, (window_width, window_height))
		Window.blit(IMAGE, (0, 0))
		pygame.display.flip()
		move_lock = True
		return
	out(field)
	last_move_tick = 0
	instant_move = False


field = GenerateBoard()
out(field)

clock = pygame.time.Clock()

run = True
last_move_tick = 0
move_speed = 30  # You can move every X ticks
instant_move = True  # True when user stops holding a key
move_lock = False
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	
	keys = pygame.key.get_pressed()
	
	if keys[pygame.K_LEFT]:
		move(field, 'Right')
	elif keys[pygame.K_RIGHT]:
		move(field, "Left")
	elif keys[pygame.K_UP]:
		move(field, "Down")
	elif keys[pygame.K_DOWN]:
		move(field, "Up")
	elif keys[pygame.K_ESCAPE]:
		run = False
	else:
		instant_move = True
	
	last_move_tick += 1
	clock.tick(120)

pygame.quit()
