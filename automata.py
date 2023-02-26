from set import Set
from estado import Estado
from simbolo import Simbolo

class Automata:
    def __init__(self):
        self.Estados = Set()
        self.EstadosFinales = Set()
        self.Simbolos = Set()
        self.estado_inicial = None
        self.transiciones = []

    def GetItem(self, id):
        for estado in self.Estados.Elementos:
            if estado.id == id:
                return estado
