class Unit:
    def __init__(self, h:int=0,d:int=0, ar:int=0, ms:int=0):
        self.health = h
        self.damage = d
        self.attack_radius = ar
        self.move_speed = ms
    
if __name__ == "__main__":
    class_u = Unit()
    dict_u = {
        "health":0,
        "damage":0,
        "attack_radius": 0,
        "move_speed": 0,
    }
    print(class_u.__sizeof__())
    print(dict_u.__sizeof__())