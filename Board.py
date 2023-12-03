from GameEl import create_element


def get_board(width, height: int) -> list[list]:
    return [[create_element() for _ in range(width)] for _ in range(height)]


def print_board(board: list[list], t: str = "consolePresent"):
    for line in board:
        for element in line:
            print(element[t], end=" ")
        print()
 

def set_element(board: list[list], element: dict, x: int, y: int):
    board[y][x] = element


def get_element(board: list[list], x: int, y: int) -> dict:
    return board[y][x]


def distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1-x2) + abs(y1-y2)


if __name__ == "__main__":
    print(distance(0, 0, 1, 1))
