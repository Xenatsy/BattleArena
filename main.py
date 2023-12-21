import tkinter
from tkinter import font
from itertools import product
from random import randint

from PIL import Image, ImageTk

"""
Let a base game element haves parameters:
    1. Health
        1.1. Current Health
    2. Damage
    3. Move speed
        1.1. leftover moves
    4. Console present
    5. GUI present
"""
###


class Unit:
    def __init__(self, **kwargs):
        self.health = kwargs["health"]
        self.currentHealth = kwargs["health"]
        self.damage = kwargs["damage"]
        self.move_speed = kwargs["move_speed"]
        self.leftoverMoves = kwargs["move_speed"]


def fight(element1: dict, element2: dict):
    element1["currentHealth"] -= element2["damage"]
    element2["currentHealth"] -= element1["damage"]


###


def get_board(width, height: int) -> list[list]:
    return [[create_element() for _ in range(width)] for _ in range(height)]


def print_board(board: list[list], t: str = "consolePresent"):
    for _ in board[0]:
        print(end="--")
    print("-")
    for line in board:
        print(end="|")
        for element in line:
            print(element[t], end="|")
        print()
        for _ in line:
            print(end="--")
        print("-")
    print()


def set_element(board: list[list], element: dict, x: int, y: int):
    board[y][x] = element


def get_element(board: list[list], x: int, y: int) -> dict:
    return board[y][x]


def delete_element(board: list[list], x: int, y: int):
    board[y][x] = create_element()


def distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)

###


def draw_board(board: list[list]):
    global resized_white_tk
    cell_size = 500 // 2 // board_size
    new_resized_white = white.resize((cell_size-1, cell_size-1))
    resized_white_tk = ImageTk.PhotoImage(new_resized_white)
    for x, y in product(range(len(board[0])), range(len(board))):
        d = dict(board[y][x])
        canvas.create_image(cell_size*x, cell_size*y, anchor="nw", image=resized_white_tk, tags=f"cell/{x}/{y}")
        if d["type"] != "empty":
            canvas.create_oval(x*cell_size, y*cell_size, (x+1)*cell_size, (y+1)*cell_size, fill=d["team"], tags=f"unit/{x}/{y}")
            board[y][x]["tag"] = f"unit/{x}/{y}"
        canvas.tag_bind(f"cell/{x}/{y}", "<Enter>", handle)
        canvas.tag_bind(f"unit/{x}/{y}", "<Enter>", handle)
        canvas.tag_bind(f"cell/{x}/{y}", "<Leave>", handle)
        canvas.tag_bind(f"unit/{x}/{y}", "<Leave>", handle)
        canvas.tag_bind(f"cell/{x}/{y}", "<Button-1>", handle)
        canvas.tag_bind(f"unit/{x}/{y}", "<Button-1>", handle)


def handle(event: tkinter.Event):
    global resized_white_tk, resized_red_tk, resized_green_tk
    x0 = min(window.winfo_width(), window.winfo_height()) // 2
    if int(event.type) != 22:
        tag = canvas.gettags("current")[0]
    w, h = resized_white_tk.width(), resized_white_tk.height()
    new_resized_red = red.resize((w, h))
    resized_red_tk = ImageTk.PhotoImage(new_resized_red)
    new_resized_green = green.resize((w, h))
    resized_green_tk = ImageTk.PhotoImage(new_resized_green)
    match int(event.type):
        case 4:  # print("Нажато")
            canvas.itemconfigure(tag.replace("unit", "cell"), image=resized_green_tk)
        case 7: # print("Наведено")
            canvas.itemconfig(tag.replace("unit", "cell"), image=resized_red_tk)
            for x, y in product(range(len(board1[0])), range(len(board1))):
                d = dict(board1[y][x])
                if d["tag"] == tag:
                    # Рисование статистики
                    canvas.itemconfig("statistic",
                                      text=f"Здоровье: {d["currentHealth"]}/{d["health"]}\n"
                                           f"Урон: {d["damage"]}\n"
                                           f"Расстояние за ход: {d["leftoverMoves"]}/{d["moveSpeed"]}"
                                       )

        case 8:  # print("Отведено")
            canvas.itemconfigure(tag.replace("unit", "cell"), image=resized_white_tk)
        case 22:
            cell_size = min(event.width, event.height) // 2 // board_size
            new_resized_white = white.resize((cell_size, cell_size))
            resized_white_tk = ImageTk.PhotoImage(new_resized_white)
            for x, y in product(range(len(board1[0])), range(len(board1))):
                d = dict(board1[y][x])
                canvas.itemconfig(f"cell/{x}/{y}", image=resized_white_tk)
                canvas.coords(f"cell/{x}/{y}", cell_size*x, cell_size*y)
                if d["type"] != "empty":
                    canvas.coords(f"unit/{x}/{y}", x*cell_size+2, y*cell_size+2, (x+1)*cell_size-2, (y+1)*cell_size-2)
                canvas.itemconfig("statistic", font=font.Font(canvas, f"Consolas {cell_size//2}"))
    canvas.coords("statistic", x0, 0)


if __name__ == "__main__":
    window = tkinter.Tk()
    window.geometry("500x500+0+0")
    board_size = 10
    board1 = get_board(board_size, board_size)
    units = []
    for side in (1, 2):
        for _ in range(5):
            element = create_element(
                health=randint(1, 100),
                damage=randint(1, 10),
                moveSpeed=randint(1, 3),
                console=["B", "W"][side-1],
                team=["#00F", "#FF0"][side-1],
                type="unit",
                tag="Hydralisk"
            )
            units.append(element)
    while len(units):
        x = randint(0, len(board1[0])-1)
        y = randint(0, len(board1)-1)
        if get_element(board1, x, y)["type"] == "empty":
            u = units.pop()
            set_element(board1, u, x, y)

    red = Image.new("RGBA", (1, 1), "#F00")
    resized_red = red.resize((1, 1))
    resized_red_tk = ImageTk.PhotoImage(resized_red)

    green = Image.new("RGBA", (1, 1), "#0F0")
    resized_green = green.resize((1, 1))
    resized_green_tk = ImageTk.PhotoImage(resized_green)

    white = Image.new("RGBA", (1, 1), "#FFF")
    resized_white = white.resize((1, 1))
    resized_white_tk = ImageTk.PhotoImage(resized_white)

    window.title("Battle Arena")
    window.geometry("500x500+0+0")
    window.resizable(True, True)
    window.bind("<Configure>", handle)

    canvas = tkinter.Canvas()

    # Рисование доски
    draw_board(board1)

    # x0 = 4*min(window.winfo_width(), window.winfo_height()) // 2
    canvas.create_text(250, 0, anchor="nw",
                       text=f"Здоровье: /\n"
                            f"Урон: \n"
                            f"Расстояние за ход: /",tags="statistic"
                       )
    canvas.pack(fill="both", expand=True)

    window.mainloop()
