from automata import Automata
from set import Set
from estado import Estado
from simbolo import Simbolo
from arbol import Nodo
from arbol import Arbol
from transicion import Transicion
from graph import Graph

'''
    Clase que representa un AFD_Minimizado. Inicializa con un automata AFD que se desea minimizar.
'''
class AFD_Minimizacion(Automata):
    def __init__(self, afd):
        # Inicializa la clase padre (Automata)
        super().__init__()
        self.afd = afd

        self.minimizar()

    # Hopcroft's algorithm: https://en.wikipedia.org/wiki/DFA_minimization
    def minimizar(self):
        F = self.afd.EstadosFinales
        Q = self.afd.Estados

        difference = Q.Diferencia(F)

        P = Set()
        P.AddItem(F)

        if not difference.IsEmpty():
            P.AddItem(difference)

        W = Set()
        W.AddItem(F)
        if not difference.IsEmpty():
            W.AddItem(difference)
        

        while not W.IsEmpty():
            A = W.returnFirstItem()
            W.deleteItem(A)

            for c in self.afd.Simbolos.Elementos:
                X = Set()

                for t in self.afd.transiciones:
                    if t.el_simbolo.id == c.id and t.estado_destino in A.Elementos:
                        X.AddItem(t.estado_origen)

                for Y in P.Elementos:
                    interseccion_empty = X.Interseccion(Y).IsEmpty()
                    diferencia_empty = Y.Diferencia(X).IsEmpty()

                    if (not interseccion_empty) and (not diferencia_empty):
                        intersection = X.Interseccion(Y)
                        difference = Y.Diferencia(X)

                        P.deleteItem(Y)
                        P.AddItem(intersection)
                        P.AddItem(difference)

                        if Y in W.Elementos:
                            W.deleteItem(Y)
                            W.AddItem(intersection)
                            W.AddItem(difference)
                        else:
                            if intersection.size() <= difference.size():
                                W.AddItem(intersection)
                            else:
                                W.AddItem(difference)

        P.Elementos.sort(key=lambda x: x.size(), reverse=False)
        P.Elementos.sort(key=lambda x: x.Elementos[0].id)

        estados_temp = []
        for enu, conjunto in enumerate(P.Elementos):

            estado_actual = Estado(enu)

            self.Estados.AddItem(estado_actual)
            estados_temp.append([estado_actual, conjunto])

            for estado in conjunto.Elementos:
                if estado in self.afd.EstadosFinales.Elementos:
                    self.EstadosFinales.AddItem(estado_actual)
                
                if estado == self.afd.estado_inicial:
                    self.estado_inicial = estado_actual

        transiciones_temp = []
        for transicion in self.afd.transiciones:
            for estado, conjunto in estados_temp:

                if transicion.estado_origen in conjunto.Elementos:

                    for estado2, conjunto2 in estados_temp:

                        if transicion.estado_destino in conjunto2.Elementos:
                            transiciones_temp.append([estado, estado2, transicion.el_simbolo])
                            break

        
        transiciones_temp = [list(x) for x in set(tuple(x) for x in transiciones_temp)]

        for estado, estado2, simbolo in transiciones_temp:
            self.transiciones.append(Transicion(estado, estado2, simbolo))


