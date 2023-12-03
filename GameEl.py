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


def get_element(health=1, damage=1, move_speed=1, console=" ", graph="") -> dict:
    return {
        "health": health,
        "currentHealth": health,
        "damage": damage,
        "moveSpeed": move_speed,
        "leftoverMoves": move_speed,
        "consolePresent": console,
        "GUIPresent": graph
    }


if __name__ == "__main__":
    pass

