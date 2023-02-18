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
        # Inicializa la clase padre (Automata)
        super().__init__()

        # Inicializa el arbol de expresiones regulares
        self.tree = tree

        # Inicializa los simbolos del arbol
        self.Simbolos = self.get_simbolos(tree)

        # Creacion del automata
        self.afn_construction(tree)

    # Obtiene los simbolos del arbol de expresiones regulares
    def get_simbolos(self, tree_node):
        simbolos = Set()
        if tree_node is not None:
            if tree_node.valor == '.' or tree_node.valor == '|' or tree_node.valor == '*':
                simbolos = simbolos.Union(self.get_simbolos(tree_node.izq))
                simbolos = simbolos.Union(self.get_simbolos(tree_node.der))
            else:
                simbolos.AddItem(tree_node.simbolo)

        simbolos_unicos = Set()
        ids = []

        for simbolo in simbolos.Elementos:
            id_simbolo = simbolo.id
            if id_simbolo not in ids:
                ids.append(id_simbolo)
                simbolos_unicos.AddItem(simbolo)
                
        return simbolos_unicos

    def afn_construction(self, nodo):
        valor, der, izq, simbolo = nodo.valor, nodo.der, nodo.izq, nodo.simbolo

        if (izq == None and der == None):
            return True

        self.afn_construction(izq)

        

        
            


            