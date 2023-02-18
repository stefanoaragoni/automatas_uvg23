from automata import Automata
from set import Set
from estado import Estado
from simbolo import Simbolo

'''
    Clase que representa un AFN. Inicializa el automata con los estados, simbolos y transiciones.
    Utiliza el arbol de expresiones regulares para construir el AFN.
'''
class AFN(Automata):
    def __init__(self, tree):
        self.tree = tree

        # Inicializa los simbolos
        for node in self.tree:
            if node.valor != '|' and node.valor != '.' and node.valor != '*' and node.valor != '+' and node.valor != '?':
                self.simbolos.add(node.simbolo)

        # Inicializa los estados
        estado_inicial = Estado(0, 0)
        self.estados.AddItem(estado_inicial)

        # Inicializa las transiciones
        self.transiciones = self.subset_construction()

    def subset_construction(self):
        pass
