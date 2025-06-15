import random
import time
from colorsys import hsv_to_rgb
from tkinter import *
import math


# Yeah this is unsalvageable, all these exec() functions are... a thing of beauty, so to speak
# Still kinda fun for a code speedrun tbh

class Rect:
	def __init__(self, canvas, id, numb, color, max_n, swap_color, check_color, completed_color):
		self.id = id
		self.numb = numb
		self.default_color = color
		self.canvas = canvas
		self.swap_color = swap_color
		self.check_color = check_color
		self.completed_color = completed_color
		self.x, self.y, self.top_x, self.top_y = canvas.coords(id)
		
		font_size = int((self.top_x - self.x) // (len(str(max_n))))  # //5 on android
		if font_size == 0:
			def nolabel_move(x, y):
				self.canvas.move(self.id, x, y)
			
			self.move = nolabel_move
			return
		
		self.num_label = canvas.create_text((self.x + self.top_x) / 2, self.top_y + font_size + 10, text=numb,
		                                    justify="center", fill="white", font=("Comic Sans MS", font_size))
	
	def change_color(self, color):
		self.canvas.itemconfig(self.id, fill=color)
	
	def set_swap_color(self):
		self.canvas.itemconfig(self.id, fill=self.swap_color)
	
	def set_completed_color(self):
		self.canvas.itemconfig(self.id, fill=self.completed_color)
	
	def set_check_color(self):
		self.canvas.itemconfig(self.id, fill=self.check_color)
	
	def reset_color(self):
		self.canvas.itemconfig(self.id, fill=self.default_color)
	
	def ret_coords(self):
		return self.canvas.coords(self.id)
	
	def move(self, x, y):
		self.canvas.move(self.id, x, y)
		self.canvas.move(self.num_label, x, y)


window = Tk()
window.config(background="black")

label_style = {"font": "Arial 16", "background": "black", "foreground": "white"}
slider_style = {"background": "black", "foreground": "white", "relief": "flat", "activebackground": "gray",
                "highlightbackground": "black"}
sortnames = ["bubbl", "selection thing", "[your add could be here] (insertion sort)", "merg"]

curr_sort_slider_label = Label(window, text="bubbl", **label_style, wraplength=150)
curr_sort_slider = Scale(window, orient=HORIZONTAL, from_=1, to=4, **slider_style, showvalue=False,
                         command=lambda currsort: curr_sort_slider_label.configure(text=sortnames[int(currsort) - 1]))
curr_sort_slider_label.grid(row=1, column=1, sticky="s")
curr_sort_slider.grid(row=1, column=2, padx=(5, 20), pady=(20, 0), sticky="s")

color_variant_slider_label = Label(window, text="color variant", **label_style)
color_variant_slider = Scale(window, orient=HORIZONTAL, from_=1, to=3, **slider_style)
color_variant_slider_label.grid(row=1, column=3, sticky="s")
color_variant_slider.grid(row=1, column=4, padx=(5, 20), pady=(20, 0), sticky="s")
color_variant_slider.set(3)

recursion_move_up_slider_label = Label(window, text="move up (on recursion)", **label_style)
recursion_move_up_sort_slider = Scale(window, orient=HORIZONTAL, from_=0, to=200, **slider_style)
recursion_move_up_slider_label.grid(row=1, column=5, sticky="s")
recursion_move_up_sort_slider.grid(row=1, column=6, padx=(5, 20), pady=(20, 0), sticky="s")
recursion_move_up_sort_slider.set(50)

sq_numb_slider_label = Label(window, text="input size", **label_style)
sq_numb_sort_slider = Scale(window, orient=HORIZONTAL, from_=1, to=1000, **slider_style)
sq_numb_slider_label.grid(row=2, column=1, sticky="s")
sq_numb_sort_slider.grid(row=2, column=2, padx=(5, 20), pady=(20, 0), sticky="s")
sq_numb_sort_slider.set(16)

speed_slider_label = Label(window, text="animation speed\n(100 is fastest)", **label_style)
speed_sort_slider = Scale(window, orient=HORIZONTAL, from_=1, to=100, **slider_style)
speed_slider_label.grid(row=2, column=3, sticky="s")
speed_sort_slider.grid(row=2, column=4, padx=(5, 20), pady=(20, 0), sticky="s")
speed_sort_slider.set(5)

rect_width_slider_label = Label(window, text="rect width", **label_style)
rect_width_sort_slider = Scale(window, orient=HORIZONTAL, from_=2, to=200, **slider_style)
rect_width_slider_label.grid(row=3, column=1, sticky="s")
rect_width_sort_slider.grid(row=3, column=2, padx=(5, 20), pady=(20, 0), sticky="s")
rect_width_sort_slider.set(40)

rect_height_slider_label = Label(window, text="rect height (per value)", **label_style)
rect_height_sort_slider = Scale(window, orient=HORIZONTAL, from_=1, to=100, **slider_style)
rect_height_slider_label.grid(row=3, column=3, sticky="s")
rect_height_sort_slider.grid(row=3, column=4, padx=(5, 20), pady=(20, 0), sticky="s")
rect_height_sort_slider.set(10)

rect_min_height_slider_label = Label(window, text="rect minheight", **label_style)
rect_min_height_sort_slider = Scale(window, orient=HORIZONTAL, from_=2, to=200, **slider_style)
rect_min_height_slider_label.grid(row=3, column=5, sticky="s")
rect_min_height_sort_slider.grid(row=3, column=6, padx=(5, 20), pady=(20, 0), sticky="s")
rect_min_height_sort_slider.set(10)

rect_offset_slider_label = Label(window, text="rectangle margin", **label_style)
rect_offset_sort_slider = Scale(window, orient=HORIZONTAL, from_=1, to=100, **slider_style)
rect_offset_slider_label.grid(row=4, column=1, sticky="s")
rect_offset_sort_slider.grid(row=4, column=2, padx=(5, 20), pady=(20, 0), sticky="s")
rect_offset_sort_slider.set(10)

offset_x_slider_label = Label(window, text="offset x", **label_style)
offset_x_sort_slider = Scale(window, orient=HORIZONTAL, from_=0, to=1000, **slider_style)
offset_x_slider_label.grid(row=4, column=3, sticky="s")
offset_x_sort_slider.grid(row=4, column=4, padx=(5, 20), pady=(20, 0), sticky="s")
offset_x_sort_slider.set(0)

offset_y_slider_label = Label(window, text="offset y", **label_style)
offset_y_sort_slider = Scale(window, orient=HORIZONTAL, from_=0, to=1000, **slider_style)
offset_y_slider_label.grid(row=4, column=5, sticky="s")
offset_y_sort_slider.grid(row=4, column=6, padx=(5, 20), pady=(20, 0), sticky="s")
offset_y_sort_slider.set(450)


def random_settings():
	curr_sort_slider.set(random.randint(curr_sort_slider.config().get("from")[-1],
	                                    curr_sort_slider.config().get("to")[-1]))
	color_variant_slider.set(random.randint(color_variant_slider.config().get("from")[-1],
	                                        color_variant_slider.config().get("to")[-1]))
	recursion_move_up_sort_slider.set(random.randint(recursion_move_up_sort_slider.config().get("from")[-1],
	                                                 recursion_move_up_sort_slider.config().get("to")[-1]))
	sq_numb_sort_slider.set(random.randint(sq_numb_sort_slider.config().get("from")[-1],
	                                       sq_numb_sort_slider.config().get("to")[-1]))
	speed_sort_slider.set(random.randint(speed_sort_slider.config().get("from")[-1],
	                                     speed_sort_slider.config().get("to")[-1]))
	rect_width_sort_slider.set(random.randint(rect_width_sort_slider.config().get("from")[-1],
	                                          rect_width_sort_slider.config().get("to")[-1]))
	rect_height_sort_slider.set(random.randint(rect_height_sort_slider.config().get("from")[-1],
	                                           rect_height_sort_slider.config().get("to")[-1]))
	rect_min_height_sort_slider.set(random.randint(rect_min_height_sort_slider.config().get("from")[-1],
	                                               rect_min_height_sort_slider.config().get("to")[-1]))
	rect_offset_sort_slider.set(random.randint(rect_offset_sort_slider.config().get("from")[-1],
	                                           rect_offset_sort_slider.config().get("to")[-1]))
	offset_x_sort_slider.set(random.randint(offset_x_sort_slider.config().get("from")[-1],
	                                        offset_x_sort_slider.config().get("to")[-1]))
	offset_y_sort_slider.set(random.randint(offset_y_sort_slider.config().get("from")[-1],
	                                        offset_y_sort_slider.config().get("to")[-1]))


random_button = Button(window, text="Hey let ME decide", **label_style, command=random_settings)
random_button.grid(row=5, column=4, columnspan=4, pady=(40, 20))


def start():
	global label_style
	animation_window = Toplevel(window, background="black")
	
	sort_name = sortnames[int(curr_sort_slider.get() - 1)]
	curr_sort = int(curr_sort_slider.get())
	color_variant = int(color_variant_slider.get())
	recursion_move_up = int(recursion_move_up_sort_slider.get())
	sq_numb = int(sq_numb_sort_slider.get())
	speed = int(speed_sort_slider.get())
	rect_width = int(rect_width_sort_slider.get())
	rect_height = int(rect_height_sort_slider.get())
	rect_min_height = int(rect_min_height_sort_slider.get())
	rect_offset = int(rect_offset_sort_slider.get())
	offsetx = int(offset_x_sort_slider.get())
	offsety = int(offset_y_sort_slider.get())
	
	animation_window.title(sort_name)
	
	algorithm_name = Label(animation_window, text=sort_name, font=("Comic Sans MS", 20), fg="white", bg="black")
	algorithm_name.pack(fill="x")
	
	canvas = Canvas(animation_window, bg="black")
	canvas.pack(fill='both', expand=True)
	
	# Init
	arr = list(range(1, sq_numb + 1))
	rects = {}
	random.shuffle(arr)
	
	if color_variant == 1:  # Original color scheme
		def get_color():
			yield "blue", "red", "#0ed400", "gold"
	
	elif color_variant == 2:  # Monotonic gradient
		def get_color():
			step = 255 / sq_numb
			
			for i in range(sq_numb):
				value = 255 - int(i * step)
				# Skew towards middle to avoid pitch black
				if value < 127:
					value += int((127 - value) ** 0.9)
				
				gradient = format(value, 'x')
				if len(gradient) == 2:
					main_color = f"#0000{gradient}"
					swap_color = f"#{gradient}0000"
					check_color = f"#00{gradient}00"
					completed_color = f"#{gradient}{gradient}00"
				else:
					main_color = f"#00000{gradient}"
					swap_color = f"#0{gradient}0000"
					check_color = f"#000{gradient}00"
					completed_color = f"#0{gradient}0{gradient}00"
			
			yield main_color, swap_color, check_color, completed_color
	
	elif color_variant == 3:  # Gradient wheel
		def generate_rgb_wheel(step: int = 1, cycles: float = 0.8, starting_hue: float = 0,
		                       max_steps: int = None) -> list:
			hue = starting_hue
			step /= 1530  # 255 * 6, technically it should be 1536 but this somehow works
			total_steps = max_steps
			step = 1 / total_steps * cycles
			
			for _ in range(total_steps):
				r, g, b = hsv_to_rgb(hue, 1, 255)
				yield round(r), round(g), round(b)
				hue += step
				if hue >= 1:
					hue -= 1
		
		def get_color():
			for r, g, b in generate_rgb_wheel(max_steps=sq_numb):
				rx, gx, bx = format(r, 'x'), format(g, 'x'), format(b, 'x')
				
				if len(rx) == 1:
					rx = f"0{rx}"
				if len(gx) == 1:
					gx = f"0{gx}"
				if len(bx) == 1:
					bx = f"0{bx}"
				
				yield f"#{rx}{gx}{bx}", "red", "#0ed400", "gold"
	
	color_generator = get_color()
	all_colors = list(next(color_generator) for i in range(sq_numb))
	# I would've liked to create them in-place, but the list is random, colors aren't
	for i, n in enumerate(arr, start=1):
		main_color, swap_color, check_color, completed_color = all_colors[n - 1]
		id = canvas.create_rectangle(offsetx + ((rect_width + rect_offset) * i), offsety,
		                             offsetx + ((rect_width + rect_offset) * i) + rect_width,
		                             offsety - rect_min_height - (rect_height * n), fill="black")
		
		rects[n] = Rect(canvas, id, n, main_color, sq_numb, swap_color, check_color, completed_color)
	# Change from rects[n] to rects[i] for a new sort - but sort, it will completely break my commands, but it will still
	# magically sort the array, no one knows how, scientist deemed this question far above our current capabilities
	# may future generations solve this mystery (def not me)
	
	rect_w = sq_numb * (rect_width + rect_offset) + offsetx + 100
	rect_h = (rect_min_height + sq_numb * rect_height) + offsety + 100
	
	animation_window.geometry(f"{min(animation_window.winfo_screenwidth() - 100, rect_w)}x"
	                          f"{min(animation_window.winfo_screenheight() - 100, rect_h)}+0+0")
	
	def reset_colors(arr=rects):
		for i in arr:
			arr[i].reset_color()
	
	def set_check_color(rect, instant=False):
		rect.set_check_color()
		if speed >= 100 or instant:
			canvas.update()
		else:
			animation_window.after(change_timing // speed, canvas.update())
	
	def set_swap_color(rect, instant=False):
		rect.set_swap_color()
		if speed >= 100 or instant:
			canvas.update()
		else:
			animation_window.after(change_timing // speed, canvas.update())
	
	def set_default_color(rect, instant=False):
		rect.reset_color()
		if speed >= 100 or instant:
			canvas.update()
		else:
			animation_window.after(change_timing // speed, canvas.update())
	
	def set_completed_color(rect, instant=False):
		rect.set_completed_color()
		if speed >= 100 or instant:
			canvas.update()
		else:
			animation_window.after(change_timing // speed, canvas.update())
	
	def recursion_move_y(arr, y):
		nonlocal speed, move_up_timing
		if speed < 100:
			for i in range(abs(y)):
				for n in arr:
					move_to_rel(rects[n], 0, -1, instant=True)
			animation_window.after(move_up_timing, canvas.update())
		else:
			for n in arr:
				move_to_rel(rects[n], 0, y)
	
	def artificial_delay(ms):
		nonlocal speed
		if speed >= 100:
			return
		animation_window.after(ms, canvas.update())
		return
	
	def move_to_rel(rect, x, y, instant=False):
		nonlocal speed, swap_timing
		
		needed_move = [x, y]
		if speed >= 100 or instant:
			# При гиперзвуковой скорости нафига визуально крутить вертеть
			rect.move(*needed_move)
			canvas.update()
			return
		
		needed_move[0] /= swap_timing // speed
		needed_move[1] /= swap_timing // speed
		
		for step in range(swap_timing // speed):
			rect.move(*needed_move)
			animation_window.after(1, canvas.update())
	
	def move_to(rect: Rect, pos):
		nonlocal speed, swap_timing
		b1pos = rect.ret_coords()
		
		xleftx, topy, xr, yd = pos
		needed_move = [xr - b1pos[2], yd - b1pos[3]]
		
		if speed >= 100:
			# При гиперзвуковой скорости нафига крутить вертеть
			rect.move(*needed_move)
			canvas.update()
			return
		
		needed_move[0] /= swap_timing // speed
		needed_move[1] /= swap_timing // speed
		
		for step in range(swap_timing // speed):
			rect.move(*needed_move)
			animation_window.after(1, canvas.update())
	
	def move_to_recursion(rect: Rect, pos, y_offset):
		curr_pos = rect.ret_coords()
		pos[3] = curr_pos[3] - y_offset
		move_to(rect, pos)
	
	def swap(rec1: Rect, rec2: Rect, docolor=True):
		nonlocal speed, swap_timing
		b1pos = rec1.ret_coords()
		b2pos = rec2.ret_coords()
		
		# b1pos = (b1pos[0]+b1pos[2])/2, b1pos[1]
		# b2pos = (b2pos[0]+b2pos[2])/2, b2pos[1]
		
		if docolor:
			rec1.set_swap_color()
			rec2.set_swap_color()
		
		# В общей сумме между ходами 1 секунда, так что анимация - 250 :
		# Y
		
		if speed >= 100:
			# При гиперзвуковой скорости нафига крутить вертеть
			rec1.move(b2pos[0] - b1pos[0], 0)
			rec2.move(b1pos[0] - b2pos[0], 0)
			canvas.update()
			return
		
		for i in range((swap_timing // 3) // speed):
			rec1.move(0, 100 / ((swap_timing // 3) // speed))
			rec2.move(0, -100 / ((swap_timing // 3) // speed))
			animation_window.after(1, canvas.update())
		
		# X
		for i in range((swap_timing // 4) // speed):
			rec1.move((b2pos[0] - b1pos[0]) / ((swap_timing // 4) // speed), 0)
			rec2.move((b1pos[0] - b2pos[0]) / ((swap_timing // 4) // speed), 0)
			animation_window.after(1, canvas.update())
		
		# Y
		for i in range((swap_timing // 3) // speed):
			rec1.move(0, -100 / ((swap_timing // 3) // speed))
			rec2.move(0, 100 / ((swap_timing // 3) // speed))
			animation_window.after(1, canvas.update())
	
	def change_color(rec1: Rect, color, instant=False):
		nonlocal speed, change_timing
		
		rec1.change_color(color)
		
		if speed >= 100 or instant:
			canvas.update()
		else:
			animation_window.after(change_timing // speed, canvas.update())
	
	def get_places(arr):
		locations = [rects[rect].ret_coords() for rect in arr]
		return locations
	
	remember_place = None
	
	def remember(value):
		nonlocal remember_place
		remember_place = value
	
	def bubl_steps(arr):
		# O(n²) time, O(1) memory
		local_steps = []
		swapped = True
		n = 0
		while swapped:
			swapped = False
			for i in range(len(arr) - 1):
				if arr[i] > arr[i + 1]:
					local_steps.append(f"swap(rects[{arr[i]}], rects[{arr[i + 1]}])")
					local_steps.append("reset_colors()")
					arr[i], arr[i + 1] = arr[i + 1], arr[i]
					
					swapped = True
					n += 1
				else:
					local_steps.append(f"set_check_color(rects[{arr[i]}])")
			
			local_steps.append("reset_colors()")
		
		local_steps.append("reset_colors()")
		return local_steps
	
	def selection_sort(arr):
		# O(n²) time, O(1) memory
		local_steps = []
		
		# Tecnically could be faster it sorted_n was changed in for cycle, not manually
		sorted_n = 0
		while sorted_n < len(arr) - 1:
			min, mini = arr[sorted_n], sorted_n
			local_steps.append(f"set_swap_color(rects[{min}])")
			for i, n in enumerate(arr[sorted_n + 1:], start=sorted_n + 1):
				local_steps.append(f"set_check_color(rects[{n}])")
				if n < min:
					local_steps.append(f"set_swap_color(rects[{n}], instant=True)")
					local_steps.append(f"set_default_color(rects[{min}])")
					min = n
					mini = i
				else:
					local_steps.append(f"artificial_delay(change_timing // 3)")
					local_steps.append(f"set_default_color(rects[{n}])")
			
			local_steps.append(f"swap(rects[{arr[sorted_n]}], rects[{arr[mini]}])")
			local_steps.append(f"set_completed_color(rects[{arr[mini]}], instant=True)")
			if sorted_n != mini:
				local_steps.append(f"set_default_color(rects[{arr[sorted_n]}], instant=True)")
			arr[sorted_n], arr[mini] = arr[mini], arr[sorted_n]
			
			sorted_n += 1
		
		local_steps.append(f"set_completed_color(rects[{arr[-1]}], instant=True)")
		local_steps.append("reset_colors()")
		return local_steps
	
	def insertion_sort(arr):
		# O(n²), O(n) best case, O(1) space
		local_steps = [f"set_completed_color(rects[{arr[0]}], instant=True)"]
		for sorted_end, n in enumerate(arr[1:]):
			if arr[sorted_end] <= n:
				local_steps.append(f"set_completed_color(rects[{n}])")
				continue
			
			j = sorted_end
			local_steps.append(f"remember(rects[{n}].ret_coords())")
			local_steps.append(f"move_to_rel(rects[{n}], 0, 100)")
			local_steps.append(f"set_swap_color(rects[{n}])")
			
			while j >= 0 and n < arr[j]:
				local_steps.append(f"local_remember = rects[{arr[j]}].ret_coords()")
				local_steps.append(f"set_swap_color(rects[{n}])")
				local_steps.append(f"move_to(rects[{arr[j]}], remember_place)")
				local_steps.append(f"set_completed_color(rects[{arr[j]}], instant=True)")
				local_steps.append(f"remember(local_remember)")
				arr[j + 1] = arr[j]
				j -= 1
			arr[j + 1] = n
			if j >= 0:
				local_steps.append(f"set_check_color(rects[{arr[j]}])")
			local_steps.append(f"move_to(rects[{n}], remember_place)")
			local_steps.append(f"set_completed_color(rects[{n}])")
			if j >= 0:
				local_steps.append(f"set_completed_color(rects[{arr[j]}], instant=True)")
		local_steps.append("reset_colors()")
		return local_steps
	
	def merge_sort(arr):
		nonlocal recursion_move_up, move_up_timing, swap_timing, speed
		
		def merge(arr1, arr2, n, m, moveto_locations):
			i, j = 0, 0
			k = 0
			temp = [0] * (n + m)
			local_steps.append(f"set_check_color(rects[{arr1[0]}], instant=True)")
			local_steps.append(f"set_check_color(rects[{arr2[0]}])")
			while i < n and j < m:
				if arr1[i] < arr2[j]:
					temp[k] = arr1[i]
					local_steps.append(
						f"move_to_recursion(rects[{arr1[i]}], {moveto_locations[k]}, {-recursion_move_up})")
					if speed < 100:
						local_steps.append(f"set_completed_color(rects[{arr1[i]}], instant=True)")
					i += 1
					if i < n:
						local_steps.append(f"set_check_color(rects[{arr1[i]}])")
						if speed < 100:
							local_steps.append(f"artificial_delay({move_up_timing})")
				else:
					temp[k] = arr2[j]
					local_steps.append(
						f"move_to_recursion(rects[{arr2[j]}], {moveto_locations[k]}, {-recursion_move_up})")
					if speed < 100:
						local_steps.append(f"set_completed_color(rects[{arr2[j]}], instant=True)")
					j += 1
					if j < m:
						local_steps.append(f"set_check_color(rects[{arr2[j]}])")
						if speed < 100:
							local_steps.append(f"artificial_delay({move_up_timing})")
				k += 1
			
			while i < n:
				temp[k] = arr1[i]
				local_steps.append(f"move_to_recursion(rects[{arr1[i]}], {moveto_locations[k]}, {-recursion_move_up})")
				local_steps.append(f"set_completed_color(rects[{arr1[i]}], instant=True)")
				i += 1
				k += 1
			while j < m:
				temp[k] = arr2[j]
				local_steps.append(f"move_to_recursion(rects[{arr2[j]}], {moveto_locations[k]}, {-recursion_move_up})")
				local_steps.append(f"set_completed_color(rects[{arr2[j]}], instant=True)")
				j += 1
				k += 1
			if speed < 100:
				local_steps.append(f"artificial_delay({move_up_timing})")
			return temp
		
		def mergeSort(arr, l, r):
			if r - l <= 1:
				return arr
			mid = (l + r) // 2
			locations = get_places(arr[l:r])
			local_steps.append(f"recursion_move_y({arr[l:mid]}, {-recursion_move_up})")
			L = mergeSort(arr[l:mid], 0, mid)
			local_steps.append(f"recursion_move_y({arr[mid:r]}, {-recursion_move_up})")
			R = mergeSort(arr[mid:r], 0, r - mid)
			
			local_steps.append(f"reset_colors()")
			return merge(L, R, mid, r - mid, locations)
		
		local_steps = []
		mergeSort(arr, 0, len(arr))
		local_steps.append(f"reset_colors()")
		return local_steps
	
	def next_step():
		# Ahh, what a beautiful sign (I know there is other way, but who cares, it's beautiful)
		nonlocal step, steps, reset_colors, set_check_color, set_swap_color, current_step_label, \
			set_default_color, set_completed_color, recursion_move_y, artificial_delay, total_steps, \
			move_to_rel, move_to, move_to_recursion, swap, change_color, get_places, remember, rects
		
		if step + 1 == len(steps):
			return
		
		step += 1
		this_step = steps[step]
		print(this_step)
		exec(this_step)
		current_step_label.configure(text=f"{step + 1}/{total_steps}")
		
		if "_color" in this_step or "recursion" in this_step:
			animation_window.after(0, next_step)
	
	def prev_step():
		nonlocal step, steps, reset_colors, set_check_color, set_swap_color, current_step_label, \
			set_default_color, set_completed_color, recursion_move_y, artificial_delay, total_steps, \
			move_to_rel, move_to, move_to_recursion, swap, change_color, get_places, remember, rects
		
		if step <= 0:
			return
		
		step -= 1
		this_step = steps[step]
		print(this_step)
		exec(this_step)
		current_step_label.configure(text=f"{step + 1}/{total_steps}")
		
		if "_color" in this_step or "recursion" in this_step:
			animation_window.after(0, prev_step)
	
	def speed_up():
		nonlocal speed, speed_up_count, animating_rn, current_speed_label
		if 1 <= speed < 100:
			if animating_rn:
				speed_up_count += 1
			else:
				speed += 1
				current_speed_label.configure(text=speed)
	
	def speed_down():
		nonlocal speed, speed_down_count, animating_rn, current_speed_label
		if speed == 100 and animating_rn:
			print("THE BREAKS ARE BROKEN, WE ARE GONNA DIE")
			return
		
		if 1 < speed <= 100:
			if animating_rn:
				speed_down_count += 1
			else:
				speed -= 1
				current_speed_label.configure(text=speed)
	
	buttons_frame = Frame(animation_window, background="black")
	
	prev_btn = Button(buttons_frame, text="Prev", command=lambda: prev_step(),
	                  width=10, height=3, bg='gray')
	prev_btn.pack(side="left", padx=(50, 0))
	current_step_label = Label(buttons_frame, **label_style)
	current_step_label.pack(side="left", padx=10)
	next_btn = Button(buttons_frame, text="Next", command=next_step, width=10, height=3, bg='gray')
	next_btn.pack(side="left", padx=(0, 50))
	
	speed_up_count = speed_down_count = 0
	
	speed_down_btn = Button(buttons_frame, text="Speed down", command=speed_down, width=10, height=3, bg='gray')
	speed_down_btn.pack(side="left", padx=(50, 0))
	current_speed_label = Label(buttons_frame, text=str(speed), **label_style)
	current_speed_label.pack(side="left", padx=10)
	speed_up_btn = Button(buttons_frame, text="Speed up", command=speed_up, width=10, height=3, bg='gray')
	speed_up_btn.pack(side="left")
	
	exit_button = Button(buttons_frame, text="Free me\nplease", command=animation_window.destroy,
	                     width=10, height=3, bg='gray')
	exit_button.pack(side="left", padx=(50, 0))
	
	buttons_frame.pack(pady=10)
	
	# Animation timings
	swap_timing = 1150
	change_timing = 500
	moveto_timing = 1000
	move_up_timing = 500
	
	start = time.time()
	
	if curr_sort == 1:
		steps = bubl_steps(arr)
	elif curr_sort == 2:
		steps = selection_sort(arr)
	elif curr_sort == 3:
		steps = insertion_sort(arr)
	elif curr_sort == 4:
		steps = merge_sort(arr)
	reset_colors()
	
	generation_time = time.time()
	
	step = 0
	total_steps = len(steps)
	current_step_label.configure(text=f"1/{total_steps}")
	# print(*steps, sep="\n")  # Why
	print("\nSteps:", total_steps)
	print("Generation:", generation_time - start, "s")
	
	print_steps = False
	animating_rn = True
	
	# It was a whole function, but it was annoying to deal with namespaces
	for step in range(step, len(steps)):
		this_step = steps[step]
		exec(this_step)
		current_step_label.configure(text=f"{step + 1}/{total_steps}")
		
		if 'instant' in this_step or speed == 100:
			continue
		
		if print_steps:
			print(this_step)  # printing is slow man, no way I let it pring when speedrunning this thing
		
		if 'swap' in this_step:
			timing = swap_timing
		elif 'change_color' in this_step:
			timing = change_timing
		elif "move_to" in this_step:
			timing = moveto_timing
		else:
			canvas.update()
			continue
		
		animation_window.after(timing // speed, canvas.update())
		
		if speed_up_count:
			speed += speed_up_count
			speed_up_count = 0
			speed = min(speed, 100)
			current_speed_label.configure(text=speed)
		elif speed_down_count:
			speed -= speed_down_count
			speed_down_count = 0
			speed = max(speed, 1)
			current_speed_label.configure(text=speed)
	animating_rn = False
	
	print("Animation:", time.time() - generation_time, "s")
	reset_colors()


start_button = Button(window, text="Start... ehh... no joke damn", **label_style, command=start)
start_button.grid(row=5, column=1, columnspan=3, pady=(40, 20))

window.mainloop()
