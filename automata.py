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
        self.first = {}
        self.follow = {}

    def GetItem(self, id):
        for estado in self.Estados.Elementos:
            if estado.id == id:
                return estado
            
    def GetTransicion(self, estado_origen, simbolo):
        for transicion in self.transiciones:
            if transicion.estado_origen == estado_origen and transicion.simbolo.id == simbolo.id:
                return transicion
            
    

