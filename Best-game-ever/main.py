from tkinter import *
import random

window = Tk()
window.geometry("1000x1000")
bts = Button(text="1", command=lambda: comma(bts), font=("Comic Sans MS", 50))
bts.place(x=0, y=0, relheight=1, relwidth=1)


def comma(button: Button):
	def gen_col():
		a = "0123456789abcdef"
		return f"#{random.choice(a)}{random.choice(a)}{random.choice(a)}{random.choice(a)}{random.choice(a)}{random.choice(a)}"
	
	text = str(int(button["text"]) + 1)
	x, y = button.winfo_x(), button.winfo_y()
	width, height = button.winfo_width() // 2, button.winfo_height() // 2
	button.destroy()
	
	font = ("Comic Sans MS", width // 2)
	
	col = gen_col()
	eeeee = Button(text=text, command=lambda: comma(eeeee), justify='center', height=height, width=width, font=font,
	               bg=col)
	eeeee.place(x=x, y=y, height=height, width=width)
	col = gen_col()
	b = Button(text=text, command=lambda: comma(b), justify='center', height=height, width=width, font=font, bg=col)
	b.place(x=x + width, y=y, height=height, width=width)
	col = gen_col()
	c = Button(text=text, command=lambda: comma(c), justify='center', height=height, width=width, font=font, bg=col)
	c.place(x=x, y=y + height, height=height, width=width)
	col = gen_col()
	d = Button(text=text, command=lambda: comma(d), justify='center', height=height, width=width, font=font, bg=col)
	d.place(x=x + width, y=y + height, height=height, width=width)


def a(weight=4):
	c = window.winfo_children()
	
	ma = max((int(i["text"]) for i in c))
	nl = [i for i in c for _ in range(weight ** (ma - int(i["text"])))]
	b = random.choice(nl)
	
	comma(b)
	
	# Тут задержка можешь творить хаос
	window.after(500, a)


window.after(500, a)

window.mainloop()
