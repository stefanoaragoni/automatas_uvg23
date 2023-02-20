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
        self.subconjuntos_transiciones = {}

        self.contador_estados = 0

        first_state = self.e_closure(afn.estado_inicial, ascii)
        first_state = sorted(first_state.Elementos, key=lambda estado: estado.id)
        first_state_temp = Set()
        first_state_temp.AddItems(first_state)
        self.subconjuntos[self.contador_estados] = first_state_temp

        # Eliminar simbolo epsilon de los simbolos del AFD
        self.Simbolos = self.afn.Simbolos

        for simbolo in self.afn.Simbolos.Elementos:
            if simbolo.id == self.ascii:
                self.Simbolos.deleteItem(simbolo)

        self.afd_construccion(first_state)

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

    def afd_construccion(self, estados):

        for simbolo in self.Simbolos.Elementos:
            estados = Set()
            self.subconjuntos_transiciones[self.contador_estados] = {}

            for estado in estados.Elementos:
                estados = estados.Union(self.e_closure(estado, simbolo.id))

            inside = False
            for element in self.subconjuntos:
                value = self.subconjuntos[element]
                if (value.Diferencia(estados)).IsEmpty():
                    inside = True

            if inside == False:
                self.subconjuntos_transiciones[self.contador_estados][simbolo] = self.contador_estados + 1
                self.contador_estados += 1
                self.subconjuntos[self.contador_estados] = estados

            

