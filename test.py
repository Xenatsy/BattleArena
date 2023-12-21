import tkinter
from PIL import Image, ImageTk


def handle(event: tkinter.Event):
    global resized_tk
    resized_image = image.resize((event.width-10, event.height-10))
    resized_tk = ImageTk.PhotoImage(resized_image)
    canvas.itemconfig("red", image=resized_tk)
    pass


window = tkinter.Tk()
window.geometry("500x500+0+0")
window.resizable(True, True)
window.bind("<Configure>", handle)

canvas = tkinter.Canvas()
image = Image.new("RGBA", (500, 500), color="#F00")
resized_image = image.resize((10, 10))
resized_tk = ImageTk.PhotoImage(resized_image)
canvas.create_image(0,0,anchor="nw", image=resized_tk, tags="red")
canvas.pack(expand=True, fill="both")

window.mainloop()
