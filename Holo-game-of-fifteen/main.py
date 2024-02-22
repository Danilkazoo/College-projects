import random
import keyboard
import pygame

pygame.init()
Window = pygame.display.set_mode((655, 655))
pygame.display.set_caption('Holotop')

imagename = 'Holo_art.jpg'
# Тупо кидаем картинку в тот же файл что и прогу
# И ставим название, усё, картинка сделана

IMAGE = pygame.image.load(imagename).convert_alpha()
IMAGE = pygame.transform.smoothscale(IMAGE, (600, 600))


def GenerateBoard():
	JopaBobra = []
	RandomNumbers = list(range(1, 16))  # Числа на доске от 1 до 15
	random.shuffle(RandomNumbers)
	RandomNumbers.append("☢")
	for i in range(4):
		JopaBobra.append([])
		for j in range(4):
			JopaBobra[i].append(RandomNumbers.pop(0))
	return JopaBobra


# Проверка победы (Не факт, мы не прошли(
def check(field):
	return (field == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, "☢"]])


def CreateSquare(x, y, Window, i):
	Image_X = (i % 4) * 150
	Image_Y = (i // 4) * 150
	
	Window.blit(IMAGE, (x, y), (Image_X, Image_Y, 150, 150))


def out(arr):
	global Window
	pygame.draw.rect(Window, (0, 0, 0), pygame.Rect(0, 0, 750, 750))
	
	for i in range(len(arr)):
		for j in range(len(arr[0])):
			if (arr[i][j] != "☢"):
				CreateSquare(j * 155 + 20, i * 155 + 20, Window, arr[i][j] - 1)
	pygame.display.update()


# Движение по Y инвертировано
def move(field, move):
	for i in range(4):
		if ("☢" in field[i]):
			y, x = i, field[i].index("☢")
	
	if (move == "Left"):
		if (x > 0):
			field[y][x - 1], field[y][x] = field[y][x], field[y][x - 1]
		else:
			print("\nДвижение недоступно\n")
			return
	
	elif (move == "Right"):
		if (x < 3):
			field[y][x + 1], field[y][x] = field[y][x], field[y][x + 1]
		else:
			print("\nДвижение недоступно\n")
			return
	
	elif (move == "Up"):
		if (y > 0):
			field[y - 1][x], field[y][x] = field[y][x], field[y - 1][x]
		else:
			print("\nДвижение недоступно\n")
			return
	
	elif (move == "Down"):
		if (y < 3):
			field[y + 1][x], field[y][x] = field[y][x], field[y + 1][x]
		else:
			print("\nДвижение недоступно\n")
			return
	
	out(field)
	
	if (check(field)):
		global Window
		
		print("ВЫ ПОБЕДИЛИ")
		
		IMAGE = pygame.image.load(imagename).convert_alpha()
		IMAGE = pygame.transform.smoothscale(IMAGE, (655, 655))
		Window.blit(IMAGE, (0, 0))
		pygame.display.flip()


field = GenerateBoard()
out(field)

keyboard.add_hotkey("Left_Arrow", lambda: move(field, "Right"))
keyboard.add_hotkey("Right_Arrow", lambda: move(field, "Left"))
keyboard.add_hotkey("Up_Arrow", lambda: move(field, "Down"))
keyboard.add_hotkey("Down_Arrow", lambda: move(field, "Up"))

keyboard.wait('esc')
pygame.quit()
