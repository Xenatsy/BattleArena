from GameEl import get_element


def get_board(width, height: int) -> list[list]:
    return [[get_element() for _ in range(width)] for _ in range(height)]


def print_board(board: list[list], t: str = "consolePresent"):
    for line in board:
        for element in line:
            print(element[t], end=" ")
        print()

def distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1-x2) + abs(y1-y2)

if __name__ == "__main__":
    print(distance(0,0,1,1))


