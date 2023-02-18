from set import Set
from estado import Estado
from simbolo import Simbolo
from transicion import Transicion

class Automata:
    def __init__(self):
        self.Estados = Set()
        self.EstadosFinales = Set()
        self.Simbolos = Set()
        self.estado_inicial = None
        self.transiciones = []

    def Transicion(self, e, s):
        estados = Set()
        for transicion in self.transiciones:
            if transicion.estado_origen == e and transicion.el_simbolo == s:
                estados.AddItem(transicion.estado_destino)
        return estados
