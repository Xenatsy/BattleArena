from GameEl import create_element


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
    return abs(x1-x2) + abs(y1-y2)


if __name__ == "__main__":
    game_board = get_board(8, 8)
    # set_element(game_board, create_element(1, 1, 1, "p"), 0, 0)
    print_board(game_board)
    # delete_element(game_board, 0, 0)
    # print_board(game_board)

