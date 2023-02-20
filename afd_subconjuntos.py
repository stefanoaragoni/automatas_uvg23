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

        first_state = self.e_closure(afn.estado_inicial, self.ascii)
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

        print("hey")

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

    def e_closure_check(self, estado, simbolo_transicion, visited = Set()):
        estados = Set()
        visited.AddItem(estado)
        check = False

        if estado not in self.afn.EstadosFinales.Elementos:
            for transicion in self.afn.transiciones:
                if (transicion.estado_origen == estado and transicion.el_simbolo.id == self.ascii):
                    nuevo_estado = transicion.estado_destino

                    if nuevo_estado not in visited.Elementos:
                        visited.AddItem(nuevo_estado)
                        if (check):
                            result = self.e_closure_check(nuevo_estado, simbolo_transicion, visited)
                            if result:
                                estados = estados.Union(result)

                if(transicion.estado_origen == estado and transicion.el_simbolo.id == simbolo_transicion):
                    nuevo_estado = transicion.estado_destino

                    if nuevo_estado not in visited.Elementos:
                        visited.AddItem(nuevo_estado)
                        result = self.e_closure_check(nuevo_estado, simbolo_transicion, visited)
                        if result:
                            estados = estados.Union(result)
                            check = True

        if check:
            return estados
        else:
            return False

    # https://www.cs.scranton.edu/~mccloske/courses/cmps260/nfa_to_dfa.html
    def afd_construccion(self):
        # Initialize the queue with the first state
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

                # Para cada estado en el conjunto actual
                for estado in estado_actual.Elementos:
                    # Obtiene el conjunto de estados alcanzables por el símbolo actual desde el estado actual
                    temporal_result = self.e_closure_check(estado, simbolo_transicion)
                    
                    if temporal_result != False:
                        # Agrega los estados alcanzables al conjunto de estados
                        estados = estados.Union(temporal_result)

                # Si el conjunto de estados no está vacío
                if estados.Elementos:

                    for i in range(0, len(self.subconjuntos)):
                        if (estados.Diferencia(self.subconjuntos[i])).Elementos != [] and (self.subconjuntos[i].Diferencia(estados)).Elementos != []:
                            self.subconjuntos[self.contador_estados] = estados
                            self.subconjuntos_transiciones.append([estado_actual_id, self.contador_estados, simbolo])
                            queue.AddItem([estados, self.contador_estados])
                            self.contador_estados += 1
                            break

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
                