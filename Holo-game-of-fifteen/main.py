import random
import keyboard
import pygame

pygame.init()
Window = pygame.display.set_mode((655, 655))
pygame.display.set_caption('Holo is top')

imagename = "Holo_art.jpg"
# Тупо кидаем картинку в тот же файл что и прогу

# НА СКОЛЬКО КУСКОВ РЕЖЕЕЕМ     (Мы заказали хороший нож)
# Сложность - тупо размер поля, норма - 4х4
Board_Width = Board_Height = 4

IMAGE = pygame.image.load(imagename).convert_alpha()
IMAGE = pygame.transform.smoothscale(IMAGE, (655, 655))


def GenerateBoard():
	JopaBobra = []
	RandomNumbers = list(range(1, (Board_Width * Board_Height)))  # Числа на доске от 1 до 15
	random.shuffle(RandomNumbers)
	RandomNumbers.append("☢")  # Пустое место
	for i in range(Board_Width):
		JopaBobra.append([])
		for j in range(Board_Height):
			JopaBobra[i].append(RandomNumbers.pop(0))
	return JopaBobra


# Проверка победы (Не факт, мы не прошли(
def check(field):
	for i in range(Board_Width):
		for j in range(Board_Height):
			if (field[i][j] != (i * Board_Height) + j + 1):
				if (i == Board_Width - 1 and j == Board_Height - 1):
					return True
				return False
	return True


def CreateSquare(x, y, Window, i, Size):
	Image_X = (i % Board_Width) * Size
	Image_Y = (i // Board_Height) * Size
	
	Window.blit(IMAGE, (x, y), (Image_X, Image_Y, Size, Size))


def out(arr):
	global Window
	if (Board_Width > Board_Height):
		Square_count = Board_Width
	else:
		Square_count = Board_Height
	pygame.draw.rect(Window, (0, 0, 0), pygame.Rect(0, 0, 655, 655))  # Чёрный квадрат на весь экран
	Square_Size = (615 - (Square_count - 1) * 5) / Square_count
	
	for i in range(len(arr)):
		for j in range(len(arr[0])):
			if (arr[i][j] != "☢"):
				CreateSquare(j * (Square_Size + 5) + 20, i * (Square_Size + 5) + 20, Window, arr[i][j] - 1, Square_Size)
	pygame.display.update()  # Обновление экрана


# Движение по Y инвертировано
def move(field, move):
	for i in range(Board_Width):
		if ("☢" in field[i]):
			y, x = i, field[i].index("☢")
	if (move == "Left"):
		if (x > 0):
			field[y][x - 1], field[y][x] = field[y][x], field[y][x - 1]
		else:
			print("\nДвижение недоступно\n")
			return
	
	elif (move == "Right"):
		if (x < Board_Width - 1):
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
		if (y < Board_Height - 1):
			field[y + 1][x], field[y][x] = field[y][x], field[y + 1][x]
		else:
			print("\nДвижение недоступно\n")
			return
	
	if (check(field)):
		global Window
		
		print("ВЫ ПОБЕДИЛИ")
		
		IMAGE = pygame.image.load(imagename).convert_alpha()
		IMAGE = pygame.transform.smoothscale(IMAGE, (655, 655))
		Window.blit(IMAGE, (0, 0))
		pygame.display.flip()
	else:
		out(field)


field = GenerateBoard()
out(field)

keyboard.add_hotkey("Left_Arrow", lambda: move(field, "Right"))
keyboard.add_hotkey("Right_Arrow", lambda: move(field, "Left"))
keyboard.add_hotkey("Up_Arrow", lambda: move(field, "Down"))
keyboard.add_hotkey("Down_Arrow", lambda: move(field, "Up"))

keyboard.wait('esc')
pygame.quit()
