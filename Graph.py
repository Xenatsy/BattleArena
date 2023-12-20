import tkinter
import

from itertools import product
from random import choice


# def handle(event):
#     window.update()
#     w, h = window.winfo_width(), window.winfo_height()
#     m = min(3*w/4, 3*h/4)
#     cw = m//bw
#     ch = m//bh
#     for x, y in product(range(bw), range(bh)):
#         canvas.coords(f"board{x}{y}", cw * x, cw * y, cw + cw * x, ch + ch * y)


def enter_handle(event: tkinter.Event):
    cell.config(file="red.png")
    canvas.itemconfig("cell", image=cell)


def leave_handle(event: tkinter.Event):
    cell.config(file="blue.png")
    canvas.itemconfig("cell", image=cell)


window = tkinter.Tk()
window.title("Battle Arena")
window.geometry("500x500+0+0")
window.resizable(True, True)
# window.bind("<Configure>", handle)

frame = tkinter.Frame()
frame.pack(fill='both', expand=True)
canvas = tkinter.Canvas(master=frame)
cell = tkinter.PhotoImage(file="red.png")
canvas.create_image(50, 50, image=cell, tags="cell")
canvas.tag_bind("cell", "<Enter>", enter_handle)
canvas.tag_bind("cell", "<Leave>", leave_handle)
canvas.pack(side="top", fill="both", expand=True)

window.mainloop()
