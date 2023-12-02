from GameEl import canon


def get_board(width, height: int) -> list[list]:
    return [[canon() for _ in range(width)] for _ in range(height)]


def print_board(board: list[list], t: str = "consolePresent"):
    for line in board:
        for element in line:
            print(element[t], end=" ")
        print()


if __name__ == "__main__":
    print_board(get_board(8, 8))


