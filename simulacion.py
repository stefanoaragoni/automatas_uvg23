class Simulacion:
    def __init__(self, automata, cadena, tipo):
        self.automata = automata
        self.cadena = cadena
        self.current = ""
        
        self.resultado = False
        
        estado_inicial = automata.estado_inicial
        self.visited = set()

        if tipo == "AFN":
            self.simularAFN(estado_inicial, cadena)
        elif tipo == "AFD":
            self.simularAFD(estado_inicial, cadena)

    def simularAFN(self, estado, cadena):
        if (estado, cadena) in self.visited:
            return
        self.visited.add((estado, cadena))
        
        primer_simbolo = cadena[0] if cadena else ''

        for transicion in self.automata.transiciones:
            if transicion.estado_origen == estado and transicion.el_simbolo.c_id == primer_simbolo:
                self.simularAFN(transicion.estado_destino, cadena[1:])

            if transicion.estado_origen == estado and transicion.el_simbolo.c_id == "ε":
                self.simularAFN(transicion.estado_destino, cadena)

        if len(cadena) == 0:
            if estado in self.automata.EstadosFinales.Elementos:
                self.resultado = True
                return
            
    def simularAFD(self, estado, cadena):
        if (estado, cadena) in self.visited:
            return
        self.visited.add((estado, cadena))
        
        primer_simbolo = cadena[0] if cadena else ''

        for transicion in self.automata.transiciones:
            if transicion.estado_origen == estado and transicion.el_simbolo.c_id == primer_simbolo:
                self.simularAFD(transicion.estado_destino, cadena[1:])

        if len(cadena) == 0:
            if estado in self.automata.EstadosFinales.Elementos:
                self.resultado = True
                return


