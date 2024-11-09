import pygame
from pygame.locals import (
	K_w, K_s, K_a, K_d,
	K_ESCAPE, QUIT,
	K_LEFT, K_RIGHT, K_UP, K_DOWN,
	K_MINUS, K_EQUALS)
import pygame_menu
import os
from math import ceil, floor

import generators
import submenu_generation as submenu
from collections import namedtuple


def draw_labyrinth(world: pygame.surface.Surface, field: list, block_size: float, empty_tile_color: tuple,
                   exit_color: tuple, offsetx: int = 0, offsety: int = 0):
	for y, row in enumerate(field):
		for x, cell in enumerate(row):
			if cell != 1:
				if cell == 0:
					pygame.draw.rect(world, empty_tile_color,
					                 pygame.Rect(offsetx + x * block_size, offsety + y * block_size, block_size,
					                             block_size))
				elif cell == 2:
					pygame.draw.rect(world, exit_color, pygame.Rect(offsetx + x * block_size, offsety + y * block_size,
					                                                block_size, block_size))


def minmax(num, min, max):
	if num < min:
		return min
	if num > max:
		return max
	return num


def start_game():
	class Player(pygame.sprite.Sprite):
		def __init__(self, size, spawn_x, spawn_y, player_color):
			super(Player, self).__init__()
			self.surf = pygame.Surface((size, size))
			self.surf.fill(player_color)
			self.rect = self.surf.get_rect()
			self.color = player_color
			self.X = spawn_x
			self.Y = spawn_y
			self.size = size
		
		def check_move(self, X, Y):
			if field[Y][X] == 1:
				return False
			return True
		
		def change_size(self, new_size):
			self.size = new_size
			self.surf = pygame.Surface((new_size, new_size))
			self.surf.fill(self.color)
			self.rect = self.surf.get_rect()
		
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
		nonlocal screen, game_running, world
		if not os.path.exists(w_image_location):
			return
		img = pygame.image.load(w_image_location).convert()
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
	
	def calc_camera(player, block_size):
		cameraX = ((player.X + 0.5) * block_size) - window_width / 2
		cameraY = ((player.Y + 0.5) * block_size) - window_height / 2
		
		if cameraX < 0:
			cameraX = 0
		elif total_world_width >= window_width and cameraX > total_world_width - window_width:
			cameraX = total_world_width - window_width
		if cameraY < 0:
			cameraY = 0
		elif total_world_height >= window_height and cameraY > total_world_height - window_height:
			cameraY = total_world_height - window_height
		
		return -cameraX, -cameraY
	
	def player_move_display(screen, world, old_X, old_Y, camera_pos):
		pygame.draw.rect(world, empty_tile_color,
		                 pygame.Rect(old_X * block_size, old_Y * block_size, block_size, block_size))
		world.blit(player.surf, (player.X * block_size, player.Y * block_size))
		
		screen.blit(world, camera_pos)
		pygame.display.flip()
	
	def draw_world():
		nonlocal total_world_width, total_world_height, world
		
		screen.fill(wall_color)
		total_world_width, total_world_height = field_width * block_size, field_height * block_size
		world = pygame.Surface((total_world_width, total_world_height))
		world.fill(wall_color)  # too lazy to optimise, so just draw entire labyrinth at once (will cause lags tho)
		
		draw_labyrinth(world, field, block_size, empty_tile_color, exit_color)
		world.blit(player.surf, (player.X * block_size, player.Y * block_size))
		camera_pos = calc_camera(player, block_size)
		screen.blit(world, camera_pos)
		pygame.display.flip()
	
	global block_size
	
	pygame.display.set_caption("AAAAAAAA")
	field_width, field_height = len(field[0]), len(field)
	
	# World and camera
	total_world_width, total_world_height = field_width * block_size, field_height * block_size  # Calculated in draw_world
	camera_width, camera_height = 10000, 10000  # How many blocks around the player will be visible
	window_width = minmax((min(camera_width, field_width) * 2 + 1) * block_size, 100, screen_width - 100)
	window_height = minmax((min(camera_height, field_height) * 2 + 1) * block_size, 100, screen_height - 100)
	max_block_size = min(window_width, window_height) // 5  # See 2 blocks to every side
	max_canv_size = 300_000_000  # Canvas can get very big for higher block sizes
	max_block_size = min(max_block_size,
	                     floor((max_canv_size / (field_height * field_width)) ** 0.5))
	
	# Initialisations
	pygame.display.set_mode((window_width, window_height))
	screen = pygame.display.set_mode((window_width, window_height))
	world = world = pygame.Surface((total_world_width, total_world_height))  # It will be created later
	player = Player(block_size, spawn_x, spawn_y, player_color)
	clock = pygame.time.Clock()
	
	# Draw the labyrinth
	draw_world()
	last_move_tick = 0
	last_zoom_tick = 0
	move_delay = 10  # in ticks (120 per second)
	zoom_delay = 12
	
	game_running = True
	while game_running:
		for event in pygame.event.get():
			if event.type == QUIT:
				game_running = False
				break
		
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[K_ESCAPE]:
			break
		
		if pressed_keys[K_MINUS] and last_zoom_tick >= zoom_delay and block_size > 1:
			block_size = floor(min(window_width, window_height) / block_size) + 2  # How many block we see + 2
			block_size = floor(min(window_width, window_height) / block_size)  # Return to normal block size
			if block_size < 1:
				block_size = 1
			player.change_size(block_size)
			draw_world()
			last_zoom_tick = -1
		elif pressed_keys[K_EQUALS] and last_zoom_tick >= zoom_delay and block_size < max_block_size:
			block_size = ceil(min(window_width, window_height) / block_size) - 2  # How many block we see - 2
			block_size = ceil(min(window_width, window_height) / block_size)  # Return to normal block size
			if block_size > max_block_size:
				block_size = max_block_size
			player.change_size(block_size)
			draw_world()
			last_zoom_tick = -1
		elif any(pressed_keys) and last_move_tick > move_delay:
			oldX, oldY = player.move(pressed_keys)
			if player.X != oldX or player.Y != oldY:
				if field[player.Y][player.X] == 2:
					win()
					break
				
				camera_pos = calc_camera(player, block_size)
				player_move_display(screen, world, oldX, oldY, camera_pos)
				last_move_tick = -1
		
		last_move_tick += 1
		last_zoom_tick += 1
		clock.tick(MAX_FPS)


def main_menu():
	def close_menu():
		nonlocal menu_running
		menu_running = False
		select_menu.disable()
	
	def exit_pygame():
		global running
		running = False
		close_menu()
	
	def switch_to_main(current_menu: pygame_menu.Menu):
		nonlocal select_menu
		select_menu.enable()
		current_menu.reset(1)
	
	def selection_check_clicks():
		nonlocal lmb_pressed_prev, select_menu_hovering_indexes
		
		lmb_pressed = pygame.mouse.get_pressed(3)[0]
		mx, my = pygame.mouse.get_pos()
		
		if mx > max_nonscroll_x or my > max_nonscroll_y:  # Check if mouse is on scrollers
			for column, row in select_menu_hovering_indexes:  # Pycharm hates it but it but these are frames list[list][frames]
				all_elements_columns[column][row].set_background_color(background_color)
				all_elements_columns[column][row].force_menu_surface_update()
			lmb_pressed_prev = lmb_pressed
			return
		
		scroll_x, scroll_y = select_menu.get_scrollarea().get_offsets()
		mx += scroll_x
		my += scroll_y
		
		touching_frames = False
		# It will not work with strange columns (not strictly horizontal), then delete second break
		for column, (bmin, bmax) in enumerate(columns_boundaries):
			if bmin <= mx <= bmax:
				for row, frame in enumerate(all_elements_columns[column]):
					if frame.get_rect().collidepoint(mx, my):
						touching_frames = True
						frame.set_background_color((55, 55, 55))  # Hover effect
						frame.force_menu_surface_update()
						select_menu_hovering_indexes.append((column, row))
						if lmb_pressed_prev is False and lmb_pressed:
							index = row * columns + column
							click_commands[index]()
							break
				break
		if not touching_frames:
			for column, row in select_menu_hovering_indexes:  # Pycharm hates it but it but these are frames list[list][frames]
				all_elements_columns[column][row].set_background_color(background_color)
				all_elements_columns[column][row].force_menu_surface_update()
		
		lmb_pressed_prev = lmb_pressed
	
	def play_generated_labyrinth(gen_field, gen_spawn_x, gen_spawn_y, gen_block_size, submenu):
		global field, spawn_x, spawn_y, block_size
		field = gen_field
		block_size = gen_block_size
		spawn_y = gen_spawn_y
		spawn_x = gen_spawn_x
		switch_to_main(submenu)
		close_menu()
	
	# Description, labyrinth; generate_new_button, parameters; param_deskription, exit
	
	menu_width, menu_height = screen_width // 1.2, screen_height - 100
	screen = pygame.display.set_mode((menu_width, menu_height))
	pygame.display.set_caption("AAAAAAAA menu")
	
	background_color = (0, 0, 0)
	main_menu_theme = pygame_menu.themes.Theme(
		background_color=background_color,
		cursor_color=(255, 255, 255),
		selection_color=(255, 255, 255),
		scrollbar_color=(39, 41, 42),
		scrollbar_slider_color=(65, 66, 67),
		scrollbar_slider_hover_color=(90, 89, 88),
		title_background_color=(47, 48, 51),
		title_font_color=(220, 220, 220),
		title_close_button=False,
		widget_font_color=(220, 220, 220)
	)
	main_menu_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
	
	select_menu = pygame_menu.Menu("", menu_width, menu_height, theme=main_menu_theme,
	                               onclose=exit_pygame, verbose=False, mouse_motion_selection=True)
	labyrinth_preview_size = 400
	showcase_block_size = 5
	showcase_wall_col = (0, 0, 0)
	hitbox_padx = 30  # Easy way to fix hitboxes
	hitbox_pady = 20
	columns = 2
	field_size = labyrinth_preview_size // showcase_block_size + 5
	max_element_width = max(labyrinth_preview_size, 450)  # margin will align all elements by this
	
	margin_x = int(max_element_width // 2)
	margin_y = max_element_width // 2
	total_row_width = int(max_element_width * columns + margin_x * columns)
	
	# I have no idea what causes this bug, but it can create an infinite recursion
	if abs(menu_width - total_row_width - 102) <= 9:
		total_row_width += 19
	
	# Submenus for generation and playing
	submenu.menu_error_init()
	original_submenu = submenu.original_labyrinth_submenu(menu_width, menu_height, exit_pygame,
	                                                      switch_to_main, play_generated_labyrinth)
	customisable_submenu = submenu.customisable_labyrinth_submenu(menu_width, menu_height, exit_pygame,
	                                                              switch_to_main, play_generated_labyrinth)
	vector_submenu = submenu.vector_labyrinth_submenu(menu_width, menu_height, exit_pygame,
	                                                  switch_to_main, play_generated_labyrinth)
	# Labyrinth elements in main choosing menu
	labyrinth = namedtuple("labyrinth", "name generator description speed parameters click_command")
	elements = [
		labyrinth("Original", lambda: generators.generate_field_original(field_size, field_size),
		          "Fast but simple, blocky generation", "5s for 1024x1024", "3 parameters",
		          click_command=lambda: select_menu._open(original_submenu)),
		labyrinth("Customisable", lambda: generators.generate_field_custom(field_size, field_size, weight_up=100,
		                                                                   random_node_chance=40,
		                                                                   use_new_generator=False),
		          "Slower than optimised", "5.5s for 1024x1024", "13 parameters",
		          click_command=lambda: select_menu._open(customisable_submenu)),
		labyrinth("Vector based",
		          lambda: generators.generate_field_vector(field_size, field_size, random_choice_chance=100,
		                                                   max_path_len=10),
		          "Very slow but can look fun", "16s for 256x256", "15 parameters",
		          click_command=lambda: select_menu._open(vector_submenu))
	]
	elements_number = len(elements)
	
	arts_row = select_menu.add.frame_h(total_row_width, labyrinth_preview_size, margin=(margin_x, 0))
	arts_row._relax = True
	numb = 0
	all_elements_columns = [[] for _ in range(columns)]  # list[list][frames]
	click_commands = []
	for index, element in enumerate(elements, start=1):
		this_lab_frame = arts_row.pack(select_menu.add.frame_v(max_element_width, max_element_width,
		                                                       border_color=(255, 255, 255), border_width=2))
		this_lab_frame._relax = True
		name_label = this_lab_frame.pack(select_menu.add.label(element.name, font_size=35),
		                                 align=pygame_menu.locals.ALIGN_CENTER)
		
		field, *_ = element.generator()
		labyrinth = pygame.surface.Surface((labyrinth_preview_size, labyrinth_preview_size))
		labyrinth.fill(showcase_wall_col)
		draw_labyrinth(labyrinth, field, showcase_block_size, empty_tile_color, exit_color)
		this_lab_frame.pack(select_menu.add.surface(labyrinth), align=pygame_menu.locals.ALIGN_CENTER)
		
		text_separator = select_menu.add.vertical_margin(labyrinth_preview_size // 10)
		
		desc_label = this_lab_frame.pack(select_menu.add.label(element.description, font_size=25))
		speed_label = this_lab_frame.pack(select_menu.add.label(element.speed, font_size=25))
		parameters_label = this_lab_frame.pack(select_menu.add.label(element.parameters, font_size=25))
		
		elements = [name_label, labyrinth, text_separator, desc_label, speed_label, parameters_label]
		frame_width = max(element.get_width() for element in elements) + hitbox_padx
		frame_height = sum(element.get_height() for element in elements) + hitbox_pady
		
		this_lab_frame.resize(frame_width, frame_height)
		all_elements_columns[numb].append(this_lab_frame)
		click_commands.append(element.click_command)
		
		horizontal_margin = max(1, margin_x - frame_width + max_element_width)
		arts_row.pack(select_menu.add.horizontal_margin(horizontal_margin))
		
		numb += 1
		if numb == columns and index != elements_number:
			select_menu.add.vertical_margin(margin_y)
			arts_row = select_menu.add.frame_h(total_row_width, labyrinth_preview_size, margin=(margin_x, 0))
			arts_row._relax = True
			numb = 0
	
	select_menu.add.vertical_margin(margin_y)
	select_menu.add.button("Exit", action=exit_pygame, font_size=40, align=pygame_menu.locals.ALIGN_CENTER)
	# Do this after creating a menu so it updates locations
	columns_boundaries = []
	for column in all_elements_columns:
		min_x, max_x = float("inf"), -float("inf")
		for frame in column:
			x1, _, x2, _ = frame.get_rect()
			min_x, max_x = min(x1, min_x), max(max_x, x1 + x2)
		columns_boundaries.append((min_x, max_x))
	max_nonscroll_x, max_nonscroll_y = select_menu.get_scrollarea().get_size(True)
	
	lmb_pressed_prev = True
	select_menu_hovering_indexes = []
	menu_running = True
	while menu_running:
		events = pygame.event.get()
		
		select_menu.draw(screen, clear_surface=True)
		select_menu.update(events)
		
		if select_menu.get_current() is select_menu:
			selection_check_clicks()
		
		pygame.display.flip()
		
		clock.tick(MAX_FPS)


if __name__ == '__main__':
	os.environ['SDL_VIDEO_WINDOW_POS'] = f"30, 30"
	pygame.init()
	
	# Global variables
	screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
	screen = pygame.display.set_mode((screen_width - 200, screen_height - 200))  # Init the screen
	clock = pygame.time.Clock()
	MAX_FPS = 120
	
	player_color = (255, 0, 0)
	empty_tile_color = (255, 255, 255)
	wall_color = (0, 0, 0)
	exit_color = (150, 150, 255)
	w_image_location = "w_image.jpeg"
	
	field = []
	block_size = 20
	exits = 1
	spawn_x, spawn_y = 5, 5
	
	running = True
	while running:
		main_menu()
		if running:
			start_game()
	
	pygame.quit()
