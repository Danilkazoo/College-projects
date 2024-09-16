import pygame
import pygame_menu
from main import minmax, draw_labyrinth
import generators

_submenu_theme = pygame_menu.themes.Theme(
	background_color=(0, 0, 0),
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
_submenu_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE

_preview_canvas_size = 500
_min_size, _max_size = 10, 1000  # Not actually minimum and maximum
_default_width = _default_height = 100
_default_block_size = 5
_default_exits = 1

_preview_bg_col = (255, 255, 255)
_preview_wall_col = (0, 0, 0)
_preview_exit_col = (150, 150, 255)

_pair_frame_height = 150
_range_width = 250

_font = None
_text = pygame.Surface((0, 0))  # Should be initialised in menu_error_init
_text_rect = (10, 240)


def menu_error_init():
	global _font, _text
	
	_font = pygame.font.Font('freesansbold.ttf', 29)
	_text = _font.render("Why would you do this to my child", True, (0, 0, 0))


def configure_entry_range_pair(entry, input_range, frame, min_val, max_val, *actions):
	entry.set_onchange(lambda value: on_entry_value_change(input_range, value, min_val, max_val, *actions))
	input_range.set_onchange(lambda value: on_range_value_change(entry, value, *actions))
	frame.pack(entry)
	frame.pack(input_range)


def on_entry_value_change(entry_range, new_value, min_val, max_val, *actions):
	entry_range.set_value(minmax(new_value, min_val, max_val))
	for action in actions:
		action()


def on_range_value_change(entry, new_value, *actions):
	entry.set_value(round(new_value))
	for action in actions:
		action()


def generate_standart_inputs(menu, menu_width, draw_preview):
	menu.add.vertical_margin(20)
	
	standart_frame = menu.add.frame_h(menu_width - 50, 160)
	standart_frame.update_position()
	# Width
	width_frame = standart_frame.pack(menu.add.frame_v(400, _pair_frame_height),
	                                  align=pygame_menu.locals.ALIGN_CENTER)
	width_entry = menu.add.text_input('Labyrinth width: ', default=_default_width, input_type="input-int",
	                                  align=pygame_menu.locals.ALIGN_RIGHT)
	width_range = menu.add.range_slider('', default=_default_width, range_values=(_min_size, _max_size),
	                                    increment=1, width=_range_width, value_format=lambda x: str(round(x)))
	configure_entry_range_pair(width_entry, width_range, width_frame, _min_size, _max_size, draw_preview)
	standart_frame.update_position()
	
	# Height
	height_frame = standart_frame.pack(menu.add.frame_v(400, _pair_frame_height),
	                                   align=pygame_menu.locals.ALIGN_CENTER)
	height_entry = menu.add.text_input('Labyrinth height: ', default=_default_height, input_type="input-int")
	height_range = menu.add.range_slider('', default=_default_height, range_values=(_min_size, _max_size),
	                                     increment=1, width=_range_width,
	                                     value_format=lambda x: str(round(x)))
	configure_entry_range_pair(height_entry, height_range, height_frame, _min_size, _max_size, draw_preview)
	
	# Block size
	block_frame = standart_frame.pack(menu.add.frame_v(250, _pair_frame_height),
	                                  align=pygame_menu.locals.ALIGN_CENTER)
	block_entry = menu.add.text_input('Tile size: ', default=_default_block_size, input_type="input-int")
	block_range = menu.add.range_slider('', default=_default_block_size, range_values=(1, 50),
	                                    increment=1, width=100, value_format=lambda x: str(round(x)))
	configure_entry_range_pair(block_entry, block_range, block_frame, 1, 50, draw_preview)
	
	# Exits
	exits_frame = standart_frame.pack(menu.add.frame_v(300, _pair_frame_height),
	                                  align=pygame_menu.locals.ALIGN_CENTER)
	exits_entry = menu.add.text_input('Exits: ', default=_default_exits, input_type="input-int")
	exits_range = menu.add.range_slider('', default=1, range_values=(1, 100),
	                                    increment=1, width=100, value_format=lambda x: str(round(x)))
	configure_entry_range_pair(exits_entry, exits_range, exits_frame, 1, 100, draw_preview)
	
	width_frame._relax = True
	height_frame._relax = True
	block_frame._relax = True
	exits_frame._relax = True
	
	return width_entry, height_entry, block_entry, exits_entry


def generate_action_buttons(menu, on_play, on_redraw, on_back):
	buttons_frame = menu.add.frame_h(500, 100, align=pygame_menu.locals.ALIGN_CENTER)
	buttons_frame._relax = True
	buttons_frame.pack(menu.add.button('Play', action=on_play, font_size=40, align=pygame_menu.locals.ALIGN_CENTER))
	buttons_frame.pack(menu.add.horizontal_margin(50))
	
	buttons_frame.pack(menu.add.button('Generate again', action=on_redraw, font_size=40,
	                                   align=pygame_menu.locals.ALIGN_CENTER))
	buttons_frame.pack(menu.add.horizontal_margin(50))
	
	buttons_frame.pack(menu.add.button('Back', action=on_back, font_size=40,
	                                   align=pygame_menu.locals.ALIGN_CENTER))


def original_labyrinth_optimised_submenu(menu_width, menu_height, on_close, on_back, on_play) -> pygame_menu.Menu:
	def draw_preview():
		nonlocal field, spawn_x, spawn_y
		block_size = int(block_entry.get_value())
		width, height = int(width_entry.get_value()), int(height_entry.get_value()),
		exits = int(exits_entry.get_value())
		
		try:
			field, spawn_x, spawn_y = generators.generate_field_original_optimised(width, height, exits)
		except ValueError:
			preview.fill((255, 0, 0))
			preview.blit(_text, _text_rect)
			return
		preview.fill(_preview_wall_col)
		draw_labyrinth(preview, field, block_size, _preview_bg_col, _preview_exit_col)
	
	orig_optimised_menu = pygame_menu.Menu("", menu_width, menu_height, theme=_submenu_theme,
	                                       onclose=on_close, verbose=False,
	                                       mouse_motion_selection=True)
	
	desc_text = """More blocky generation, has a lot of strange 1 block paths, easy to predict.
	4.9s for 1024x1024"""
	name_label = orig_optimised_menu.add.label("Optimised original", font_size=50,
	                                           align=pygame_menu.locals.ALIGN_CENTER)
	desc_label = orig_optimised_menu.add.label(desc_text, font_size=30, align=pygame_menu.locals.ALIGN_CENTER)
	orig_optimised_menu.add.vertical_margin(40)
	
	# Labyrinth preview
	field, spawn_x, spawn_y = generators.generate_field_original_optimised(_default_width, _default_height,
	                                                                       _default_exits)
	preview = pygame.surface.Surface((_preview_canvas_size, _preview_canvas_size))
	orig_optimised_menu.add.surface(preview, align=pygame_menu.locals.ALIGN_CENTER)
	orig_optimised_menu.add.vertical_margin(20)
	
	# Standard values
	width_entry, height_entry, block_entry, exits_entry = generate_standart_inputs(orig_optimised_menu, menu_width,
	                                                                               draw_preview)
	# Buttons
	orig_optimised_menu.add.vertical_margin(20)
	generate_action_buttons(orig_optimised_menu,
	                        lambda: on_play(field, spawn_x, spawn_y, int(block_entry.get_value()), orig_optimised_menu),
	                        draw_preview, lambda: on_back(orig_optimised_menu))
	
	draw_preview()
	return orig_optimised_menu


def original_labyrinth_submenu(menu_width, menu_height, on_close, on_back, on_play) -> pygame_menu.Menu:
	def draw_preview():
		nonlocal field, spawn_x, spawn_y
		block_size = int(block_entry.get_value())
		width, height = int(width_entry.get_value()), int(height_entry.get_value()),
		exits = int(exits_entry.get_value())
		
		try:
			field, spawn_x, spawn_y = generators.generate_field_original(width, height, exits)
		except ValueError:
			preview.fill((255, 0, 0))
			preview.blit(_text, _text_rect)
			return
		preview.fill(_preview_wall_col)
		draw_labyrinth(preview, field, block_size, _preview_bg_col, _preview_exit_col)
	
	original_menu = pygame_menu.Menu("", menu_width, menu_height, theme=_submenu_theme,
	                                 onclose=on_close, verbose=False,
	                                 mouse_motion_selection=True)
	
	desc_text = """Squiggly generation, not that hard to predict, paths change direction a lot.
	Works well with strange labyrinth sizes.\nVery random generation speed, 40s for 1024x1024. Works similarly to dfs."""
	name_label = original_menu.add.label("Original generator", font_size=50, align=pygame_menu.locals.ALIGN_CENTER)
	desc_label = original_menu.add.label(desc_text, font_size=30, align=pygame_menu.locals.ALIGN_CENTER)
	original_menu.add.vertical_margin(40)
	
	# Labyrinth preview
	field, spawn_x, spawn_y = generators.generate_field_original(_default_width, _default_height, _default_exits)
	preview = pygame.surface.Surface((_preview_canvas_size, _preview_canvas_size))
	original_menu.add.surface(preview, align=pygame_menu.locals.ALIGN_CENTER)
	original_menu.add.vertical_margin(20)
	
	# Standard values
	width_entry, height_entry, block_entry, exits_entry = generate_standart_inputs(original_menu, menu_width,
	                                                                               draw_preview)
	# Buttons
	original_menu.add.vertical_margin(20)
	generate_action_buttons(original_menu,
	                        lambda: on_play(field, spawn_x, spawn_y, int(block_entry.get_value()), original_menu),
	                        draw_preview, lambda: on_back(original_menu))
	
	draw_preview()
	return original_menu


def customisable_labyrinth_submenu(menu_width, menu_height, on_close, on_back, on_play) -> pygame_menu.Menu:
	def draw_preview():
		nonlocal field, spawn_x, spawn_y
		block_size = int(block_entry.get_value())
		width, height = int(width_entry.get_value()), int(height_entry.get_value()),
		exits = int(exits_entry.get_value())
		
		l_weight, mid_weight, r_weight = int(l_weight_entry.get_value()), int(mid_weight_entry.get_value()), int(
			r_weight_entry.get_value())
		centered_spawn = bool(spawn_switch.get_value())
		bfs = bool(bfs_switch.get_value())
		random_node_chance = int(random_node_entry.get_value())
		dead_end_chance = int(dead_end_entry.get_value())
		guaranteed_generations = int(guaranteed_entry.get_value())
		
		try:
			field, spawn_x, spawn_y = generators.generate_field_custom(width, height, exits, l_weight, r_weight,
			                                                           mid_weight, centered_spawn, bfs,
			                                                           random_node_chance, dead_end_chance,
			                                                           guaranteed_generations)
		except ValueError:
			preview.fill((255, 0, 0))
			preview.blit(_text, _text_rect)
			return
		preview.fill(_preview_wall_col)
		draw_labyrinth(preview, field, block_size, _preview_bg_col, _preview_exit_col)
	
	custom_menu = pygame_menu.Menu("", menu_width, menu_height, theme=_submenu_theme,
	                               onclose=on_close, verbose=False, mouse_motion_selection=True)
	
	desc_text = """Slower than simple generator.
	5.5s for 1024x1024 (way slower with random node selection - 10s)."""
	name_label = custom_menu.add.label("Customisable generator", font_size=50, align=pygame_menu.locals.ALIGN_CENTER)
	desc_label = custom_menu.add.label(desc_text, font_size=30, align=pygame_menu.locals.ALIGN_CENTER)
	custom_menu.add.vertical_margin(40)
	
	# Labyrinth preview
	field, spawn_x, spawn_y = generators.generate_field_custom(_default_width, _default_height, _default_exits, )
	preview = pygame.surface.Surface((_preview_canvas_size, _preview_canvas_size))
	custom_menu.add.surface(preview, align=pygame_menu.locals.ALIGN_CENTER)
	
	# Standard values
	width_entry, height_entry, block_entry, exits_entry = generate_standart_inputs(custom_menu, menu_width,
	                                                                               draw_preview)
	
	# Weights
	first_row = custom_menu.add.frame_h(menu_width - 50, 160)
	first_row.update_position()
	l_weight_frame = first_row.pack(custom_menu.add.frame_v(300, _pair_frame_height),
	                                align=pygame_menu.locals.ALIGN_CENTER)
	l_weight_entry = custom_menu.add.text_input('Weight left: ', default=1, input_type="input-int",
	                                            align=pygame_menu.locals.ALIGN_RIGHT)
	l_weight_range = custom_menu.add.range_slider('', default=1, range_values=(1, 100), increment=1, width=150,
	                                              value_format=lambda x: str(round(x)))
	configure_entry_range_pair(l_weight_entry, l_weight_range, l_weight_frame, 1, 100, draw_preview)
	first_row.update_position()
	
	mid_weight_frame = first_row.pack(custom_menu.add.frame_v(300, _pair_frame_height),
	                                  align=pygame_menu.locals.ALIGN_CENTER)
	mid_weight_entry = custom_menu.add.text_input('Weight front: ', default=1, input_type="input-int",
	                                              align=pygame_menu.locals.ALIGN_RIGHT)
	mid_weight_range = custom_menu.add.range_slider('', default=1, range_values=(1, 100), increment=1,
	                                                width=150, value_format=lambda x: str(round(x)))
	configure_entry_range_pair(mid_weight_entry, mid_weight_range, mid_weight_frame, 1, 100, draw_preview)
	first_row.update_position()
	
	r_weight_frame = first_row.pack(custom_menu.add.frame_v(300, _pair_frame_height),
	                                align=pygame_menu.locals.ALIGN_CENTER)
	r_weight_entry = custom_menu.add.text_input('Weight right: ', default=1, input_type="input-int",
	                                            align=pygame_menu.locals.ALIGN_RIGHT)
	r_weight_range = custom_menu.add.range_slider('', default=1, range_values=(1, 100), increment=1, width=150,
	                                              value_format=lambda x: str(round(x)))
	configure_entry_range_pair(r_weight_entry, r_weight_range, r_weight_frame, 1, 100, draw_preview)
	first_row.update_position()
	
	# Other
	other_frame = first_row.pack(custom_menu.add.frame_v(300, _pair_frame_height),
	                             align=pygame_menu.locals.ALIGN_CENTER)
	
	spawn_switch = custom_menu.add.toggle_switch('', default=False, state_text=("Random start", "Start center"),
	                                             width=235, onchange=lambda _: draw_preview())
	other_frame.pack(spawn_switch)
	
	bfs_switch = custom_menu.add.toggle_switch('', default=False, state_text=("DFS", "BFS"), width=100,
	                                           onchange=lambda _: draw_preview())
	other_frame.pack(bfs_switch)
	first_row.update_position()
	
	# Node selection
	second_row = custom_menu.add.frame_h(menu_width - 50, 160)
	second_row.update_position()
	
	random_node_frame = second_row.pack(custom_menu.add.frame_v(400, _pair_frame_height),
	                                    align=pygame_menu.locals.ALIGN_CENTER)
	random_node_entry = custom_menu.add.text_input('Random node chance: ', default=0, input_type="input-int",
	                                               align=pygame_menu.locals.ALIGN_RIGHT)
	random_node_range = custom_menu.add.range_slider('', default=0, range_values=(0, 100), increment=1,
	                                                 width=_range_width, value_format=lambda x: str(round(x)))
	configure_entry_range_pair(random_node_entry, random_node_range, random_node_frame, 0, 100, draw_preview)
	second_row.update_position()
	
	dead_end_frame = second_row.pack(custom_menu.add.frame_v(400, _pair_frame_height),
	                                 align=pygame_menu.locals.ALIGN_CENTER)
	dead_end_entry = custom_menu.add.text_input('Dead end chance: ', default=0, input_type="input-int",
	                                            align=pygame_menu.locals.ALIGN_RIGHT)
	dead_end_range = custom_menu.add.range_slider('', default=0, range_values=(0, 100), increment=1, width=_range_width,
	                                              value_format=lambda x: str(round(x)))
	configure_entry_range_pair(dead_end_entry, dead_end_range, dead_end_frame, 0, 100, draw_preview)
	second_row.update_position()
	
	guaranteed_frame = second_row.pack(custom_menu.add.frame_v(500, _pair_frame_height),
	                                   align=pygame_menu.locals.ALIGN_CENTER)
	guaranteed_entry = custom_menu.add.text_input('Guaranteed generations: ', default=10, input_type="input-int",
	                                              align=pygame_menu.locals.ALIGN_RIGHT)
	guaranteed_range = custom_menu.add.range_slider('', default=10, range_values=(0, 1000), increment=1,
	                                                width=350, value_format=lambda x: str(round(x)))
	configure_entry_range_pair(guaranteed_entry, guaranteed_range, guaranteed_frame, 0, 1000, draw_preview)
	second_row.update_position()
	
	# Buttons
	custom_menu.add.vertical_margin(20)
	generate_action_buttons(custom_menu,
	                        lambda: on_play(field, spawn_x, spawn_y, int(block_entry.get_value()), custom_menu),
	                        draw_preview, lambda: on_back(custom_menu))
	
	# For very big inputs (I don't want to add constrains)
	l_weight_frame._relax = True
	mid_weight_frame._relax = True
	r_weight_frame._relax = True
	random_node_frame._relax = True
	dead_end_frame._relax = True
	guaranteed_frame._relax = True
	
	draw_preview()
	return custom_menu


def vector_labyrinth_submenu(menu_width, menu_height, on_close, on_back, on_play) -> pygame_menu.Menu:
	def draw_preview():
		nonlocal field, spawn_x, spawn_y
		block_size = int(block_entry.get_value())
		width, height = int(width_entry.get_value()), int(height_entry.get_value()),
		exits = int(exits_entry.get_value())
		
		wall_width = int(wall_width_entry.get_value())
		path_width = int(path_width_entry.get_value())
		max_path_len = int(max_path_len_entry.get_value())
		min_path_len = int(min_path_len_entry.get_value())
		centered_spawn = bool(spawn_switch.get_value())
		bfs = bool(bfs_switch.get_value())
		random_node_chance = int(random_node_entry.get_value())
		dead_end_chance = int(dead_end_entry.get_value())
		guaranteed_generations = int(guaranteed_entry.get_value())
		check_angle_step = int(check_angle_step_entry.get_value())
		ignore_tiles_radius = int(ignore_tiles_rad_entry.get_value())
		
		try:
			field, spawn_x, spawn_y = generators.generate_field_vector(width, height, wall_width, path_width,
			                                                           max_path_len, min_path_len, check_angle_step,
			                                                           ignore_tiles_radius, exits, centered_spawn, bfs,
			                                                           random_node_chance, dead_end_chance,
			                                                           guaranteed_generations)
		except ValueError:
			preview.fill((255, 0, 0))
			preview.blit(_text, _text_rect)
			return
		preview.fill(_preview_wall_col)
		draw_labyrinth(preview, field, block_size, _preview_bg_col, _preview_exit_col)
	
	custom_menu = pygame_menu.Menu("", menu_width, menu_height, theme=_submenu_theme,
	                               onclose=on_close, verbose=False, mouse_motion_selection=True)
	
	desc_text = """Very slow, works by selecting a random vector,
	and creating a wall in that direction.
	?s for 1024x1024"""
	name_label = custom_menu.add.label("Vector based generator", font_size=50, align=pygame_menu.locals.ALIGN_CENTER)
	desc_label = custom_menu.add.label(desc_text, font_size=30, align=pygame_menu.locals.ALIGN_CENTER)
	custom_menu.add.vertical_margin(40)
	
	# Labyrinth preview
	field, spawn_x, spawn_y = generators.generate_field_custom(_default_width, _default_height, _default_exits, )
	preview = pygame.surface.Surface((_preview_canvas_size, _preview_canvas_size))
	custom_menu.add.surface(preview, align=pygame_menu.locals.ALIGN_CENTER)
	
	# Standard values
	width_entry, height_entry, block_entry, exits_entry = generate_standart_inputs(custom_menu, menu_width,
	                                                                               draw_preview)
	
	# Paths and walls
	first_row = custom_menu.add.frame_h(menu_width - 50, 160)
	first_row.update_position()
	wall_width_frame = first_row.pack(custom_menu.add.frame_v(250, _pair_frame_height),
	                                  align=pygame_menu.locals.ALIGN_CENTER)
	wall_width_entry = custom_menu.add.text_input('Wall width: ', default=1, input_type="input-int",
	                                              align=pygame_menu.locals.ALIGN_RIGHT)
	wall_width_range = custom_menu.add.range_slider('', default=1, range_values=(1, 20), increment=1, width=50,
	                                                value_format=lambda x: str(round(x)))
	configure_entry_range_pair(wall_width_entry, wall_width_range, wall_width_frame, 1, 20, draw_preview)
	first_row.update_position()
	
	path_width_frame = first_row.pack(custom_menu.add.frame_v(250, _pair_frame_height),
	                                  align=pygame_menu.locals.ALIGN_CENTER)
	path_width_entry = custom_menu.add.text_input('Path width: ', default=1, input_type="input-int",
	                                              align=pygame_menu.locals.ALIGN_RIGHT)
	path_width_range = custom_menu.add.range_slider('', default=1, range_values=(1, 20), increment=1,
	                                                width=50, value_format=lambda x: str(round(x)))
	configure_entry_range_pair(path_width_entry, path_width_range, path_width_frame, 1, 20, draw_preview)
	first_row.update_position()
	
	min_path_len_frame = first_row.pack(custom_menu.add.frame_v(400, _pair_frame_height),
	                                    align=pygame_menu.locals.ALIGN_CENTER)
	min_path_len_frame._relax = True
	min_path_len_entry = custom_menu.add.text_input('Minimum path length: ', default=1, input_type="input-int",
	                                                align=pygame_menu.locals.ALIGN_RIGHT)
	min_path_len_range = custom_menu.add.range_slider('', default=1, range_values=(1, 20), increment=1, width=50,
	                                                  value_format=lambda x: str(round(x)))
	configure_entry_range_pair(min_path_len_entry, min_path_len_range, min_path_len_frame, 1, 20, draw_preview)
	first_row.update_position()
	
	max_path_len_frame = first_row.pack(custom_menu.add.frame_v(400, _pair_frame_height),
	                                    align=pygame_menu.locals.ALIGN_CENTER)
	max_path_len_frame._relax = True
	max_path_len_entry = custom_menu.add.text_input('Maximum path length: ', default=1000, input_type="input-int",
	                                                align=pygame_menu.locals.ALIGN_RIGHT)
	max_path_len_range = custom_menu.add.range_slider('', default=1000, range_values=(2, 1000), increment=1, width=150,
	                                                  value_format=lambda x: str(round(x)))
	configure_entry_range_pair(max_path_len_entry, max_path_len_range, max_path_len_frame, 1, 10000, draw_preview)
	first_row.update_position()
	
	# Node selection
	second_row = custom_menu.add.frame_h(menu_width - 50, 160)
	second_row.update_position()
	
	random_node_frame = second_row.pack(custom_menu.add.frame_v(400, _pair_frame_height),
	                                    align=pygame_menu.locals.ALIGN_CENTER)
	random_node_entry = custom_menu.add.text_input('Random node chance: ', default=0, input_type="input-int",
	                                               align=pygame_menu.locals.ALIGN_RIGHT)
	random_node_range = custom_menu.add.range_slider('', default=0, range_values=(0, 100), increment=1,
	                                                 width=_range_width, value_format=lambda x: str(round(x)))
	configure_entry_range_pair(random_node_entry, random_node_range, random_node_frame, 0, 100, draw_preview)
	second_row.update_position()
	
	dead_end_frame = second_row.pack(custom_menu.add.frame_v(400, _pair_frame_height),
	                                 align=pygame_menu.locals.ALIGN_CENTER)
	dead_end_entry = custom_menu.add.text_input('Dead end chance: ', default=0, input_type="input-int",
	                                            align=pygame_menu.locals.ALIGN_RIGHT)
	dead_end_range = custom_menu.add.range_slider('', default=0, range_values=(0, 100), increment=1, width=_range_width,
	                                              value_format=lambda x: str(round(x)))
	configure_entry_range_pair(dead_end_entry, dead_end_range, dead_end_frame, 0, 100, draw_preview)
	second_row.update_position()
	
	guaranteed_frame = second_row.pack(custom_menu.add.frame_v(500, _pair_frame_height),
	                                   align=pygame_menu.locals.ALIGN_CENTER)
	guaranteed_entry = custom_menu.add.text_input('Guaranteed generations: ', default=10, input_type="input-int",
	                                              align=pygame_menu.locals.ALIGN_RIGHT)
	guaranteed_range = custom_menu.add.range_slider('', default=10, range_values=(0, 1000), increment=1,
	                                                width=350, value_format=lambda x: str(round(x)))
	configure_entry_range_pair(guaranteed_entry, guaranteed_range, guaranteed_frame, 0, 1000, draw_preview)
	second_row.update_position()
	
	# Other
	third_row = custom_menu.add.frame_h(menu_width - 50, 160)
	third_row.update_position()
	toggles_frame = third_row.pack(custom_menu.add.frame_v(300, _pair_frame_height),
	                               align=pygame_menu.locals.ALIGN_CENTER)
	
	check_angle_step_frame = third_row.pack(custom_menu.add.frame_v(500, _pair_frame_height),
	                                        align=pygame_menu.locals.ALIGN_CENTER)
	check_angle_step_entry = custom_menu.add.text_input('Check angle step: ', default=90, input_type="input-int",
	                                                    align=pygame_menu.locals.ALIGN_RIGHT)
	check_angle_step_range = custom_menu.add.range_slider('', default=90, range_values=(1, 359), increment=1,
	                                                      width=350, value_format=lambda x: str(round(x)))
	configure_entry_range_pair(check_angle_step_entry, check_angle_step_range, check_angle_step_frame, 1, 359,
	                           draw_preview)
	third_row.update_position()
	
	ignore_tiles_rad_frame = third_row.pack(custom_menu.add.frame_v(500, _pair_frame_height),
	                                        align=pygame_menu.locals.ALIGN_CENTER)
	ignore_tiles_rad_entry = custom_menu.add.text_input('Ignore tiles radius: ', default=3, input_type="input-int",
	                                                    align=pygame_menu.locals.ALIGN_RIGHT)
	ignore_tiles_rad_range = custom_menu.add.range_slider('', default=3, range_values=(0, 10), increment=1,
	                                                      width=50, value_format=lambda x: str(round(x)))
	configure_entry_range_pair(ignore_tiles_rad_entry, ignore_tiles_rad_range, ignore_tiles_rad_frame, 0, 10,
	                           draw_preview)
	third_row.update_position()
	
	spawn_switch = custom_menu.add.toggle_switch('', default=False, state_text=("Random start", "Start center"),
	                                             width=235, onchange=lambda _: draw_preview())
	toggles_frame.pack(spawn_switch)
	
	bfs_switch = custom_menu.add.toggle_switch('', default=False, state_text=("DFS", "BFS"), width=100,
	                                           onchange=lambda _: draw_preview())
	toggles_frame.pack(bfs_switch)
	
	third_row.update_position()
	
	# Buttons
	custom_menu.add.vertical_margin(20)
	generate_action_buttons(custom_menu,
	                        lambda: on_play(field, spawn_x, spawn_y, int(block_entry.get_value()), custom_menu),
	                        draw_preview, lambda: on_back(custom_menu))
	
	# For very big inputs (I don't want to add constrains)
	wall_width_frame._relax = True
	path_width_frame._relax = True
	random_node_frame._relax = True
	dead_end_frame._relax = True
	guaranteed_frame._relax = True
	check_angle_step_frame._relax = True
	ignore_tiles_rad_frame._relax = True
	toggles_frame._relax = True
	
	draw_preview()
	return custom_menu
