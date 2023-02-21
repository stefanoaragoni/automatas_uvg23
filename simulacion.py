class Simulacion:
    def __init__(self, automata, cadena):
        self.automata = automata
        self.cadena = cadena
        self.current = ""
        
        self.resultado = False
        
        estado_inicial = automata.estado_inicial
        self.visited = set()
        self.simular(estado_inicial, cadena)

    def simular(self, estado, cadena):
        if (estado, cadena) in self.visited:
            return
        self.visited.add((estado, cadena))
        
        primer_simbolo = cadena[0] if cadena else ''

        for transicion in self.automata.transiciones:
            if transicion.estado_origen == estado and transicion.el_simbolo.c_id == primer_simbolo:
                self.simular(transicion.estado_destino, cadena[1:])

            if transicion.estado_origen == estado and transicion.el_simbolo.c_id == "ε":
                self.simular(transicion.estado_destino, cadena)

        if len(cadena) == 0:
            if estado in self.automata.EstadosFinales.Elementos:
                self.resultado = True
                return


