class Simulacion:
    def __init__(self, automata, cadena, tipo, header=None, trailer=None):
        self.automata = automata
        self.cadena = cadena
        self.current = ""
        
        self.resultado = None
        
        estado_inicial = automata.estado_inicial
        self.visited = set()

        if tipo == "AFN":
            self.simularAFN(estado_inicial, cadena)
        elif tipo == "AFD":
            self.simularAFD(estado_inicial, cadena)
        elif tipo == "Yalex":
            self.simularAFD_Yalex(estado_inicial, cadena, header, trailer)

    def simularAFN(self, estado, cadena):
        if (estado, cadena) in self.visited:
            return
        self.visited.add((estado, cadena))

        for transicion in self.automata.transiciones:

            largo_compuesto = len(transicion.el_simbolo.c_id)
            primer_simbolo = cadena[0:largo_compuesto] if cadena else ''

            if transicion.estado_origen == estado and transicion.el_simbolo.c_id == primer_simbolo:
                self.simularAFN(transicion.estado_destino, cadena[largo_compuesto:])

            if transicion.estado_origen == estado and transicion.el_simbolo.c_id == "ε":
                self.simularAFN(transicion.estado_destino, cadena)

        if len(cadena) == 0:
            if estado in self.automata.EstadosFinales.Elementos:
                self.resultado = True
                return
            
    def simularAFD(self, estado, cadena):
        if len(cadena) != 0:

            for transicion in self.automata.transiciones:

                if transicion.estado_origen == estado and transicion.el_simbolo.id.replace("'", "") == str(ord(cadena[0])):
                    self.simularAFD(transicion.estado_destino, cadena[1:])

        if len(cadena) == 0:
            self.resultado = estado
            return
            
    def simularAFD_Yalex(self, estado, cadena, header, trailer):

        current_state = estado
        last_result = None
        char_set = []
        resultado = []
        result_token = None

        for head in header:
            exec(head)

        for i, char in enumerate(cadena):

            self.simularAFD(current_state, char)

            while True:

                if self.resultado:
                    current_state = self.resultado
                    char_set.append(char)
                    self.resultado = None
                    last_result = True

                    if i == len(cadena) - 1:
                        token = ''.join(char_set)
                        temp_token = (current_state.token.id).replace("'","").replace('"', "'").replace("#", "")
                        globals_dict = {"token": token}
                        exec(temp_token, globals_dict)
                        result_token = globals_dict.get('result_token', None)
                        resultado.append([result_token, token])

                    break

                elif last_result and self.resultado == None:
                    token = ''.join(char_set)
                    temp_token = (current_state.token.id).replace("'","").replace('"', "'").replace("#", "")
                    globals_dict = {"token": token}
                    exec(temp_token, globals_dict)
                    result_token = globals_dict.get('result_token', None)
                    resultado.append([result_token, token])

                    current_state = estado
                    char_set = []
                    last_result = False

                    self.simularAFD(current_state, char)

                else:
                    resultado.append(["Error Lexico", char])
                    break

        for trail in trailer:
            exec(trail)

        self.resultado = resultado





            

            



