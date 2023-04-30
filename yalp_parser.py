from set import Set
from simbolo import Simbolo
from postfix import Postfix
from arbol import Arbol
from graph import Graph
from prettytable import PrettyTable

class YalParser():
    def __init__(self, file):

        self.file = file
        self.regex = ""

        # Contiene los caracteres que se pueden usar en la expresión regular
        self.charset = ["[", "]", "-"]
        self.define = ["(", ")"]
        self.operators = ["*", "+", "?", "|"]
        self.literal = ["'", '"']

        self.tokens = []
        self.productions = []

        self.parse()

    def parse(self):

        tokens_array = []
        productions_array = []

        # abrir archivo yal
        with open(self.file, "r") as archivo:
            file = archivo.read()

        comment = 0

        # revisar a que corresponde cada linea
        file.strip()

        # Limpieza de comentarios
        temporal_line = ""

        for i, char in enumerate(file):
            if i+1 < len(file):
                if char == "/" and file[i+1] == "*":
                    comment = 2

                elif char == "*" and file[i+1] == "/" and comment == 2:
                    comment = comment - 1

            if char == "/" and comment == 1:
                if file[i-1] == "*":
                    comment = comment - 1

            elif comment == 0:
                temporal_line += char

        file = temporal_line

        temporal_line = ""
        producciones = False

        # separar en tokens y productions
        for i, char in enumerate(file):

            if producciones == False:

                if temporal_line == "%%":
                    producciones = True
                    temporal_line = ""
                    continue

                if char == "\n":
                    temporal_line = temporal_line.strip()
                    if temporal_line != "":    
                        tokens_array.append(temporal_line)
                        temporal_line = ""

                else:
                    temporal_line += char

            elif producciones == True:
                
                if char == ";":
                    temporal_line = temporal_line.strip()
                    if temporal_line != "":    
                        productions_array.append(temporal_line)
                        temporal_line = ""

                else:
                    if char != "\n" or char != "\t":
                        temporal_line += char

        print("\BREAKPOINT - SEPARACION DE TOKENS Y PRODUCCIONES (DIRTY)")

        # LIMPIEZA DE TOKENS
        for i, token in enumerate(tokens_array):
            tokens_array[i] = token.strip()

            token_temp = []
            temporal_token = ""
            indicator = ""
            error_indicator = False

            for j, char in enumerate(tokens_array[i]):

                if char == " ":
                    error_indicator = False
                    if temporal_token != "":
                        token_temp.append(temporal_token.strip())
                        temporal_token = ""
                
                elif error_indicator == False:
                    temporal_token += char

                        
                if temporal_token == "%token":
                    indicator = "token"
                    temporal_token = ""

                    if tokens_array[i][j+1] == " ":
                        continue
                    else:
                        print("Error Lexico la linea", i+1, "de", self.file + ": Se esperaba un espacio después de %token.")
                        error_indicator = True

                elif temporal_token == "IGNORE":
                    indicator = "ignore"
                    temporal_token = ""

                    if tokens_array[i][j+1] == " ":
                        continue
                    else:
                        print("Error Lexico la linea", i+1, "de", self.file + ": Se esperaba un espacio después de IGNORE.")
                        error_indicator = True

            if temporal_token != "":
                token_temp.append(temporal_token)

            if indicator == 'token':
                for token in token_temp:
                    self.tokens.append([token,0])

            elif indicator == 'ignore':
                for token in token_temp:
                    found = False

                    for i, element in enumerate(self.tokens):
                        if element[0] == token:
                            self.tokens[i][1] = 1
                            found = True

                    if found == False:
                        print("Error Semantico la linea", i+1, "de", self.file + ": El token", token, "no ha sido declarado. No se puede 'IGNORE'.")

        for token_element in self.tokens:
            token_element[0] = token_element[0].upper()

        print("\BREAKPOINT - TOKENS LIMPIOS")

        # LIMPIEZA DE PRODUCCIONES
        for i, production in enumerate(productions_array):
            production = production.strip()

            production_temp = []
            temporal_production = ""
            name = ""
            error_indicator = False

            for j, char in enumerate(production):
                
                if char == ":":
                    error_indicator = False
                    if temporal_production != "":
                        name = temporal_production.strip()
                        temporal_production = ""
                
                elif error_indicator == False:
                    if char == "\n":
                        continue

                    elif len(temporal_production)-1 >= 0 and char == " ":
                        if temporal_production[len(temporal_production)-1] == " ":
                            continue

                    temporal_production += char

            temporal_production = temporal_production.strip()

            new_temporal_production = ""
            for j, char in enumerate(temporal_production):

                if char == "|":
                    if temporal_production != "":
                        self.productions.append([name, new_temporal_production.strip()])
                        new_temporal_production = ""

                else:
                    new_temporal_production += char

            if new_temporal_production != "":
                self.productions.append([name, new_temporal_production.strip()])

            print("\BREAKPOINT - PRODUCCIONES LIMPIAS")

                


    
                    


YalParser = YalParser("./yalex/test.yalp")