import tkinter
from tkinter import font
from itertools import product
from random import randint
from dataclasses import dataclass

from PIL import Image, ImageTk

"""
Let a base game element haves parameters:
    1. health
        1.1. Current health
    2. Damage
    3. Move speed
        1.1. leftover moves
    4. Console present
    5. GUI present
"""


###

@dataclass
class Unit:
    health: int = 0
    current_health: int = 0
    damage: int = 0
    move_speed: int = 0
    leftoverMoves: int = 0
    team: str = ""
    type: str = ""
    console: str = " "
    tag: str = ""

    def fight(self, other: "Unit"):
        self.current_health -= other.damage
        other.current_health -= self.damage

    def __repr__(self):
        return self.console


###

class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board: list[list] = self.create_elements()

    def create_elements(self):
        return [[Unit(type="empty") for _ in range(self.width)] for _ in range(self.height)]

    def print_board(self):
        for _ in range(self.height):
            print(end="--")
        print("-")
        for line in self.board:
            print(end="|")
            for element in line:
                print(element, end="|")
            print()
            for _ in line:
                print(end="--")
            print("-")
        print()

    def set_element(self, u: Unit, x: int, y: int):
        self.board[y][x] = u

    def get_element(self, x: int, y: int) -> Unit:
        return self.board[y][x]

    def delete_element(self, x: int, y: int):
        self.board[y][x] = Unit()

    @staticmethod
    def distance(x1: int, y1: int, x2: int, y2: int) -> int:
        return abs(x1 - x2) + abs(y1 - y2)

###

def draw_board(board: Board):
    global resized_white_tk
    cell_size = 500 // 2 // board_size
    new_resized_white = white.resize((cell_size - 1, cell_size - 1))
    resized_white_tk = ImageTk.PhotoImage(new_resized_white)
    for x, y in product(range(board.width), range(board.height)):
        d = board.get_element(x,y)
        canvas.create_image(cell_size * x, cell_size * y, anchor="nw", image=resized_white_tk, tags=f"cell/{x}/{y}")
        if d.type != "empty":
            canvas.create_oval(x*cell_size, y*cell_size, (x+1)*cell_size, (y+1)*cell_size, fill=d.team, tags=f"unit/{x}/{y}")
            board.get_element(x,y).tag = f"unit/{x}/{y}"
        canvas.tag_bind(f"cell/{x}/{y}", "<Enter>", handle)
        canvas.tag_bind(f"unit/{x}/{y}", "<Enter>", handle)
        canvas.tag_bind(f"cell/{x}/{y}", "<Leave>", handle)
        canvas.tag_bind(f"unit/{x}/{y}", "<Leave>", handle)
        canvas.tag_bind(f"cell/{x}/{y}", "<Button-1>", handle)
        canvas.tag_bind(f"unit/{x}/{y}", "<Button-1>", handle)


def handle(event: tkinter.Event):
    global resized_white_tk, resized_red_tk, resized_green_tk
    x0 = min(window.winfo_width(), window.winfo_height()) // 2
    w, h = resized_white_tk.width(), resized_white_tk.height()
    new_resized_red = red.resize((w, h))
    resized_red_tk = ImageTk.PhotoImage(new_resized_red)
    new_resized_green = green.resize((w, h))
    resized_green_tk = ImageTk.PhotoImage(new_resized_green)
    match int(event.type):
        case 4:  # print("Нажато")
            tag = canvas.gettags("current")[0]
            canvas.itemconfigure(tag.replace("unit", "cell"), image=resized_green_tk)
        case 7:  # print("Наведено")
            tag = canvas.gettags("current")[0]
            canvas.itemconfig(tag.replace("unit", "cell"), image=resized_red_tk)
            for x, y in product(range(board1.width), range(board1.height)):
                d = board1.get_element(x, y)
                if d.tag == tag:
                    # Рисование статистики
                    canvas.itemconfig("statistic",
                                      text=f"Здоровье: {d.current_health}/{d.health}\n"
                                           f"Урон: {d.damage}\n"
                                           f"Расстояние за ход: {d.leftoverMoves}/{d.move_speed}"
                                      )

        case 8:  # print("Отведено")
            tag = canvas.gettags("current")[0]
            canvas.itemconfigure(tag.replace("unit", "cell"), image=resized_white_tk)
            canvas.itemconfig("statistic", text="")

        case 22:
            cell_size = min(event.width, event.height) // 2 // board_size
            new_resized_white = white.resize((cell_size, cell_size))
            resized_white_tk = ImageTk.PhotoImage(new_resized_white)
            for x, y in product(range(board1.width), range(board1.height)):
                d = board1.get_element(x, y)
                canvas.itemconfig(f"cell/{x}/{y}", image=resized_white_tk)
                canvas.coords(f"cell/{x}/{y}", cell_size * x, cell_size * y)
                if d.type != "empty":
                    canvas.coords(f"unit/{x}/{y}", x * cell_size + 2, y * cell_size + 2, (x + 1) * cell_size - 2,
                                  (y + 1) * cell_size - 2)
                canvas.itemconfig("statistic", font=font.Font(canvas, f"Consolas {cell_size // 2}"))
    canvas.coords("statistic", x0, 0)


if __name__ == "__main__":
    window = tkinter.Tk()
    window.geometry("500x500+0+0")
    board_size = 10
    board1 = Board(board_size, board_size)
    units = []
    for side in (1, 2):
        for _ in range(5):
            health = randint(1, 300)
            v = randint(1, 3)
            unit = Unit(
                health=health,
                damage=randint(1, 30),
                move_speed=v,
                console=["B", "W"][side - 1],
                team=["#00F", "#FF0"][side - 1],
                type="unit",
                current_health=health,
                leftoverMoves=v
            )
            print(unit.current_health)
            units.append(unit)
    while len(units):
        x = randint(0, board1.width - 1)
        y = randint(0, board1.height - 1)
        if board1.get_element(x, y).type == "empty":
            u = units.pop()
            board1.set_element(u, x, y)
    # board1.print_board()
    print("END")

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
                            f"Расстояние за ход: /", tags="statistic"
                       )
    canvas.pack(fill="both", expand=True)

    window.mainloop()
