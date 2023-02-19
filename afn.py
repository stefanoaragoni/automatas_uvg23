from automata import Automata
from set import Set
from estado import Estado
from simbolo import Simbolo
from arbol import Nodo
from transicion import Transicion

'''
    Clase que representa un AFN. Inicializa el automata con los estados, simbolos y transiciones.
    Utiliza el arbol de expresiones regulares para construir el AFN.
'''
class AFN(Automata):
    def __init__(self, tree):
        # Inicializa la clase padre (Automata)
        super().__init__()

        # Contador de estados
        self.count_estados = 0

        # Inicializa el arbol de expresiones regulares
        self.tree = tree

        # Inicializa los simbolos del arbol
        self.Simbolos = self.get_simbolos(tree)

        # Creacion del automata
        self.afn_construction(self.tree)
        self.estados_calc()
        print("DONE")

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

    def estados_calc(self):
        # Determinar estado final
        for estado in self.Estados.Elementos:

            check = True
            for transicion in self.transiciones:

                if transicion.estado_origen.id == estado.id:
                    check = False
                
            if check == True:
                self.EstadosFinales.AddItem(estado)

        # Determinar estado inicial
        for estado in self.Estados.Elementos:

            check = True
            for transicion in self.transiciones:

                if transicion.estado_destino.id == estado.id:
                    check = False

            if check == True:
                self.estado_inicial = estado

    def afn_construction(self, padre):
        hijoIzq = padre.izq
        hijoDer = padre.der

        if padre.valor == '.':
            return self.afn_concatenacion(hijoIzq, hijoDer)

        elif padre.valor == '|':
            return self.afn_or(hijoIzq, hijoDer)

        elif padre.valor == '*':
            return self.afn_cerradura(hijoIzq)

        else:
            self.afn_simbolo(padre)

    def afn_simbolo(self, simbolo):
        a = Estado(self.count_estados)
        self.count_estados += 1

        b = Estado(self.count_estados)
        self.count_estados += 1

        ascii = ord(simbolo.valor)
        simbolo = Simbolo(ascii, simbolo.valor)

        return a, b, simbolo

    def afn_concatenacion(self, hojaIzq, hojaDer):
        hijoIzqHojaIzq = hojaIzq.izq
        hijoIzqHojaDer = hojaDer.izq

        if hijoIzqHojaIzq is None and hijoIzqHojaDer is None:
            a1, b1, s1 = self.afn_simbolo(hojaIzq)
            a2, b2, s2 = self.afn_simbolo(hojaDer)

            self.transiciones.append(Transicion(a1, b1, s1))
            self.transiciones.append(Transicion(b1, a2, s2))

            self.Estados.AddItem(a1)
            self.Estados.AddItem(b1)
            self.Estados.AddItem(a2)

            self.count_estados -= 1

            return a1, a2, s2

        if hijoIzqHojaIzq is not None and hijoIzqHojaDer is None:
            
            a1, b1, s1 = self.afn_construction(hojaIzq)
            a2, b2, s2 = self.afn_simbolo(hojaDer)

            self.transiciones.append(Transicion(b1, a2, s2))
            self.Estados.AddItem(b1)
            self.Estados.AddItem(a2)
            self.count_estados -= 1
            return b1, a2, s2

        if hijoIzqHojaIzq is None and hijoIzqHojaDer is not None:
            
            a1, b1, s1 = self.afn_simbolo(hojaIzq)
            a2, b2, s2 = self.afn_construction(hojaDer)

            self.transiciones.append(Transicion(b1, a2, s1))
            self.Estados.AddItem(b1)
            self.Estados.AddItem(a2)
            return b1, b2, s2

        if hijoIzqHojaIzq is not None and hijoIzqHojaDer is not None:
            
            a1, b1, s1 = self.afn_construction(hojaIzq)
            a2, b2, s2 = self.afn_construction(hojaDer)

            # find transicion that goes to b1 using s1
            trans_temp = None
            for transicion in self.transiciones:
                if transicion.estado_destino == b1 and transicion.el_simbolo.id == s1.id:
                    transicion.estado_destino = a2
                    self.Estados.deleteItem(b1)
                    
            return a2, b2, s2

    def afn_or(self, hojaIzq, hojaDer):
        hijoIzqHojaIzq = hojaIzq.izq
        hijoIzqHojaDer = hojaDer.izq

        t0 = Estado(self.count_estados)
        self.count_estados += 1
        self.Estados.AddItem(t0)

        ascii = ord('ε')
        simbolo = Simbolo(ascii, 'ε')

        if hijoIzqHojaIzq is None and hijoIzqHojaDer is None:
            a1, b1, s1 = self.afn_simbolo(hojaIzq)
            a2, b2, s2 = self.afn_simbolo(hojaDer)

            t1 = Estado(self.count_estados)
            self.count_estados += 1
            self.Estados.AddItem(t1)

            self.transiciones.append(Transicion(t0, a1, simbolo))
            self.transiciones.append(Transicion(t0, a2, simbolo))

            self.transiciones.append(Transicion(a1, b1, s1))
            self.transiciones.append(Transicion(a2, b2, s2))

            self.transiciones.append(Transicion(b1, t1, simbolo))
            self.transiciones.append(Transicion(b2, t1, simbolo))

            self.Estados.AddItem(a1)
            self.Estados.AddItem(a2)
            self.Estados.AddItem(b1)
            self.Estados.AddItem(b2)

            return t0, t1, simbolo

        if hijoIzqHojaIzq is not None and hijoIzqHojaDer is None:
            
            a1, b1, s1 = self.afn_construction(hojaIzq)
            a2, b2, s2 = self.afn_simbolo(hojaDer)

            t1 = Estado(self.count_estados)
            self.count_estados += 1
            self.Estados.AddItem(t1)

            self.transiciones.append(Transicion(t0, a1, simbolo))
            self.transiciones.append(Transicion(t0, a2, simbolo))

            self.transiciones.append(Transicion(a2, b2, s2))

            self.transiciones.append(Transicion(b1, t1, simbolo))
            self.transiciones.append(Transicion(b2, t1, simbolo))

            self.Estados.AddItem(a1)
            self.Estados.AddItem(a2)
            self.Estados.AddItem(b1)
            self.Estados.AddItem(b2)

            return t0, t1, simbolo

        if hijoIzqHojaIzq is None and hijoIzqHojaDer is not None:
            
            a1, b1, s1 = self.afn_simbolo(hojaIzq)
            a2, b2, s2 = self.afn_construction(hojaDer)

            t1 = Estado(self.count_estados)
            self.count_estados += 1
            self.Estados.AddItem(t1)

            self.transiciones.append(Transicion(t0, a1, simbolo))
            self.transiciones.append(Transicion(t0, a2, simbolo))

            self.transiciones.append(Transicion(a1, b1, s1))

            self.transiciones.append(Transicion(b1, t1, simbolo))
            self.transiciones.append(Transicion(b2, t1, simbolo))

            self.Estados.AddItem(a1)
            self.Estados.AddItem(a2)
            self.Estados.AddItem(b1)
            self.Estados.AddItem(b2)

            return t0, t1, simbolo

        if hijoIzqHojaIzq is not None and hijoIzqHojaDer is not None:
            
            a1, b1, s1 = self.afn_construction(hojaIzq)
            a2, b2, s2 = self.afn_construction(hojaDer)

            t1 = Estado(self.count_estados)
            self.count_estados += 1
            self.Estados.AddItem(t1)

            self.transiciones.append(Transicion(t0, a1, simbolo))
            self.transiciones.append(Transicion(t0, a2, simbolo))

            self.transiciones.append(Transicion(b1, t1, simbolo))
            self.transiciones.append(Transicion(b2, t1, simbolo))

            self.Estados.AddItem(a1)
            self.Estados.AddItem(a2)
            self.Estados.AddItem(b1)
            self.Estados.AddItem(b2)

            return t0, t1, simbolo

    def afn_cerradura(self, hojaIzq):
        hijoIzqHojaIzq = hojaIzq.izq

        t0 = Estado(self.count_estados)
        self.count_estados += 1
        self.Estados.AddItem(t0)

        ascii = ord('ε')
        simbolo = Simbolo(ascii, 'ε')

        if hijoIzqHojaIzq is None:
            
            a1, b1, s1 = self.afn_simbolo(hojaIzq)

            t1 = Estado(self.count_estados)
            self.count_estados += 1
            self.Estados.AddItem(t1)

            self.transiciones.append(Transicion(t0, t1, simbolo))
            self.transiciones.append(Transicion(t0, a1, simbolo))

            self.transiciones.append(Transicion(a1, b1, s1))
            self.transiciones.append(Transicion(b1, a1, simbolo))

            self.transiciones.append(Transicion(b1, t1, simbolo))

            self.Estados.AddItem(a1)
            self.Estados.AddItem(b1)

            return t0, t1, simbolo

        if hijoIzqHojaIzq is not None:
            
            a1, b1, s1 = self.afn_construction(hojaIzq)

            t1 = Estado(self.count_estados)
            self.count_estados += 1
            self.Estados.AddItem(t1)

            self.transiciones.append(Transicion(t0, t1, simbolo))
            self.transiciones.append(Transicion(t0, a1, simbolo))

            self.transiciones.append(Transicion(b1, a1, simbolo))
            self.transiciones.append(Transicion(b1, t1, simbolo))

            self.Estados.AddItem(a1)
            self.Estados.AddItem(b1)

            return t0, t1, simbolo
