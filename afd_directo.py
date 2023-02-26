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
        self.arbol.root.nullable_calc(self.arbol.root)
        # calcular firstpos
        self.arbol.root.firstpos_calc(self.arbol.root)
        # calcular lastpos
        self.arbol.root.lastpos_calc(self.arbol.root)
        # calcular followpos
        self.arbol.root.followpos_calc(self.arbol.root)

        # simbolos de transicion
        self.simbolos = self.get_simbolos(self.arbol.root)

        # Imprimir followpos-es
        #self.arbol.root.print_info_direct_tree(self.arbol.root)

        # Construir el automata
        self.construccion()


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
            if id_simbolo not in ids and id_simbolo != ord('ε') and id_simbolo != ord('#'):
                ids.append(id_simbolo)
                simbolos_unicos.AddItem(simbolo)
                
        return simbolos_unicos

    def construccion(self):
        uid_hashtag = self.arbol.root.der.id
        
        # Inicializar el estado inicial
        dfa_estado_inicial = [0, [self.arbol.root.firstpos, False]]
        dstates = [dfa_estado_inicial]
        dtran = []

        contador_estados = 1

        for dstate in dstates:
            dstate[1][1] = True

            for simbolo in self.simbolos.Elementos:
                
                union = Set()
                for pos in dstate[1][0].Elementos:
                    estado = self.arbol.root.find_node_by_id(self.arbol.root, pos)
                    if estado.valor == simbolo.c_id:
                        union = union.Union(estado.followpos)

                if len(union.Elementos) != 0:
                    inside = False
                    for dstate2 in dstates:
                        if union.Equals(dstate2[1][0]):
                            inside = True
                    
                    if not inside:
                        dstates.append([contador_estados, [union, False]])
                        contador_estados += 1

                for dstate2 in dstates:
                    if union.Equals(dstate2[1][0]):
                        dtran.append([dstate[0], dstate2[0], simbolo])
                        break


        # Crear los estados
        for dstate in dstates:
            estado_temp = Estado(dstate[0])

            if uid_hashtag in dstate[1][0].Elementos:
                self.EstadosFinales.AddItem(estado_temp)

            if dstate[0] == 0:
                self.estado_inicial = estado_temp

            self.Estados.AddItem(Estado(dstate[0]))

        # Crear las transiciones
        for transicion in dtran:
            estado_origen = self.GetItem(transicion[0])
            estado_destino = self.GetItem(transicion[1])
            simbolo = transicion[2]

            self.transiciones.append(Transicion(estado_origen, estado_destino, simbolo))

        
