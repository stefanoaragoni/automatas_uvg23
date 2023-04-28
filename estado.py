from set import Set

class Estado:
    def __init__(self, id, transiciones = Set()):
        self.id = id
        self.token = None
