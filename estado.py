from set import Set

class Estado:
    def __init__(self, id, tipo):
        self.id = id
        self.tipo = tipo
        self.EstadosAFN = Set()
