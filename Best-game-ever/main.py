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
	
	a = Button(text=text, command=lambda: comma(a), justify='center', height=height, width=width, font=font,
	           bg=gen_col())
	a.place(x=x, y=y, height=height, width=width)
	
	b = Button(text=text, command=lambda: comma(b), justify='center', height=height, width=width, font=font,
	           bg=gen_col())
	b.place(x=x + width, y=y, height=height, width=width)
	
	c = Button(text=text, command=lambda: comma(c), justify='center', height=height, width=width, font=font,
	           bg=gen_col())
	c.place(x=x, y=y + height, height=height, width=width)
	
	d = Button(text=text, command=lambda: comma(d), justify='center', height=height, width=width, font=font,
	           bg=gen_col())
	d.place(x=x + width, y=y + height, height=height, width=width)


def auto(weight=4):
	c = window.winfo_children()
	
	ma = max((int(i["text"]) for i in c))
	nl = [i for i in c for _ in range(weight ** (ma - int(i["text"])))]
	b = random.choice(nl)
	
	comma(b)
	
	window.after(delay, auto)


delay = -1  # Delay between auto clicks

if delay > 0:
	window.after(delay, auto)
window.mainloop()
