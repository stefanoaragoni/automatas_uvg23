from automata import Automata
from set import Set
from estado import Estado
from simbolo import Simbolo
from arbol import Nodo
from arbol import Arbol
from transicion import Transicion
from graph import Graph

'''
    Clase que representa un AFD_Directo. Inicializa el automata con los estados, simbolos y transiciones.
    Utiliza un arbol de expresiones regulares para construir el automata.
'''
class AFD_Directo(Automata):
    def __init__(self, arbol):
        # Inicializa la clase padre (Automata)
        super().__init__()

        self.arbol = arbol.arbol_directo()

        # calcular nullable
        arbol.root.nullable_calc(self.arbol.root)
        # calcular firstpos
        arbol.root.firstpos_calc(self.arbol.root)
        # calcular lastpos
        arbol.root.lastpos_calc(self.arbol.root)
        # calcular followpos
        arbol.root.followpos_calc(self.arbol.root)

        arbol.root.print_info_direct_tree(self.arbol.root)
        


        self.construccion()

    def construccion(self):
        pass
        




