from automata import Automata
from set import Set
from estado import Estado
from simbolo import Simbolo
from arbol import Nodo
from transicion import Transicion

'''
    Clase que representa un AFD_Subconjunto. Inicializa el automata con los estados, simbolos y transiciones.
    Utiliza un AFN para generar el AFD_Subconjunto.
'''
class AFD_Subconjuntos(Automata):
    def __init__(self, afn):
        # Inicializa la clase padre (Automata)
        super().__init__()
        
        self.ascii = ord('ε')

        self.afn = afn
        self.subconjuntos = {}
        self.subconjuntos_transiciones = []

        self.contador_estados = 0

        first_state = self.e_closure_check(afn.estado_inicial, self.ascii)
        first_state = sorted(first_state.Elementos, key=lambda estado: estado.id)
        first_state_temp = Set()
        first_state_temp.AddItems(first_state)
        self.subconjuntos[self.contador_estados] = first_state_temp
        self.contador_estados += 1

        # Eliminar simbolo epsilon de los simbolos del AFD
        self.Simbolos = self.afn.Simbolos

        for simbolo in self.afn.Simbolos.Elementos:
            if simbolo.id == self.ascii:
                self.Simbolos.deleteItem(simbolo)

        self.afd_construccion()

    def e_closure(self, estado, simbolo_transicion):
        estados = Set()
        estados.AddItem(estado)

        visited = Set()
        visited.AddItem(estado)

        for transicion in self.afn.transiciones:
            if (transicion.estado_origen == estado and transicion.el_simbolo.id == self.ascii) or (transicion.estado_origen == estado and transicion.el_simbolo.id == simbolo_transicion):
                nuevo_estado = transicion.estado_destino

                if nuevo_estado not in visited.Elementos:
                    visited.AddItem(nuevo_estado)
                    estados = estados.Union(self.e_closure(nuevo_estado, simbolo_transicion))

        return estados

    def e_closure_check(self, estado, simbolo_transicion):
        visited = Set()
        stack = [estado]
        result = Set()

        while stack:
            estado = stack.pop()
            if estado in visited.Elementos:
                continue
            visited.AddItem(estado)
            result.AddItem(estado)

            for transicion in self.afn.transiciones:
                if transicion.estado_origen == estado:
                    if (transicion.el_simbolo.id == self.ascii and transicion.estado_destino != estado and transicion.estado_destino not in visited.Elementos):
                        stack.append(transicion.estado_destino)

        return result


    # https://www.cs.scranton.edu/~mccloske/courses/cmps260/nfa_to_dfa.html
    def afd_construccion(self):
        current_state_id = 0
        first_state = [self.subconjuntos[current_state_id], current_state_id]

        # Inicializa la cola con el primer estado
        queue = Set()
        queue.AddItem(first_state)

        self.estado_inicial = Estado(current_state_id)

        # Mientras la cola tenga elementos
        while queue.Elementos:
            # Obtiene el primer estado de la cola
            current_state = queue.Elementos[0]
            queue.deleteItem(current_state)

            # Obtiene el primer estado del conjunto actual
            estado_actual = current_state[0]
            estado_actual_id = current_state[1]

            # Para cada símbolo del alfabeto del AFD
            for simbolo in self.Simbolos.Elementos:
                simbolo_transicion = simbolo.id

                # Inicializa el conjunto de estados
                estados = Set()

                # Buscamos elemento con transicion con simbolo
                for transicion in self.afn.transiciones:
                    if (transicion.el_simbolo.id == simbolo_transicion) and (transicion.estado_origen in estado_actual.Elementos):

                        temporal_result = self.e_closure_check(transicion.estado_destino, simbolo_transicion)
                        estados = estados.Union(temporal_result)


                if estados.size() != 0:
                    verificador = []
                    for subconjunto in self.subconjuntos:
                        elementos_subconjunto = (self.subconjuntos[subconjunto])
                        
                        verificador_subconjunto = elementos_subconjunto.size()
                        # Verificar si todos los elementos del estado actual son iguales a los elementos del subconjunto
                        
                        if estados.size() == elementos_subconjunto.size():
                            for estado in estados.Elementos:
                                if estado in elementos_subconjunto.Elementos:
                                    verificador_subconjunto -= 1
                                
                        verificador.append(verificador_subconjunto)
                        
                    if 0 not in verificador:
                        self.subconjuntos[self.contador_estados] = estados
                        self.subconjuntos_transiciones.append([estado_actual_id, self.contador_estados, simbolo])
                        queue.AddItem([estados, self.contador_estados])
                        self.contador_estados += 1
                    else:
                        index = verificador.index(0)
                        self.subconjuntos_transiciones.append([estado_actual_id, index, simbolo])

        # Agrega los estados finales
        for i in range(0, len(self.subconjuntos)):
            self.Estados.AddItem(Estado(i))
            for estado in self.subconjuntos[i].Elementos:
                if estado in self.afn.EstadosFinales.Elementos:
                    self.EstadosFinales.AddItem(Estado(i))
                    break

        # Agrega las transiciones
        for transicion in self.subconjuntos_transiciones:
            a = None
            b = None
            for estado in self.Estados.Elementos:
                if estado.id == transicion[0]:
                    a = estado
                if estado.id == transicion[1]:
                    b = estado

            self.transiciones.append(Transicion(a, b, transicion[2]))
                