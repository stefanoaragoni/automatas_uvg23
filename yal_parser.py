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

        self.lets = {}
        self.tokens = {}

        self.parse()
        self.expand_lets()

        self.generate_regex()

    def parse(self):

        let_array = []
        tokens_array = []

        # abrir archivo yal
        with open(self.file, "r") as file:
            rules = False

            # revisar a que corresponde cada linea
            for line in file:
                line = line.strip()

                if line == "":
                    pass

                # let = | se agrega a let_array
                elif line.startswith("let"):
                    let_array.append((line[4:]).strip())
                
                # rule = | se activa rules
                elif line.startswith("rule"):
                    rules = True

                # tokens = | se agrega a tokens_array
                elif rules:
                    tokens_array.append(line)

        
        # Limpieza de let_array. 
        # Resultado deseado: {regla: contenido}

        for i in range(len(let_array)):

            current_line = let_array[i]
            new_line = ""

            # elimina comentarios
            comentario = False
            for i, char in enumerate(current_line):
                
                if i+1 < len(current_line):
                    if char == "(" and current_line[i+1] == "*":
                        comentario = True

                    elif char == "*" and current_line[i+1] == ")":
                        comentario = False

                if not comentario:
                    new_line += char

            # separa contenido en nombre y contenido
            new_line = new_line.split("=")
            new_line[0] = new_line[0].strip()
            new_line[1] = new_line[1].strip()

            # almacena en diccionario
            self.lets[new_line[0]] = new_line[1]

        print(self.lets)

        # Limpieza de tokens_array.
        # Resultado deseado: {token: 'return X'}"}}
        for i in range(len(tokens_array)):
            current_line = tokens_array[i]
            new_line = ""

            comentario = 0
            for i, char in enumerate(current_line):
                
                # elimina comentarios
                if i+1 < len(current_line):
                    if char == "(" and current_line[i+1] == "*":
                        comentario = 2

                    elif char == "*" and current_line[i+1] == ")":
                        comentario = comentario - 1

                # elimina comentarios
                comment_ended = False
                if i-1 >= 0:
                    if char == ")" and current_line[i-1] == "*":
                        comentario = comentario - 1
                        comment_ended = True

                # elimina comentarios
                if comentario == 0 and not comment_ended:
                    if (char == '|' and i == 0):
                        pass
                    else:
                        new_line += char

            new_line = new_line.strip()

            elements = ["",""]

            temp_word = ""
            return_flag = False

            # separa contenido en nombre y contenido
            for char2 in new_line:

                if temp_word == "return":
                    temp_word = ""
                    return_flag = True
                    pass
                
                elif char2 == " " and not return_flag:
                    if temp_word != "":
                        elements[0] = temp_word
                        temp_word = ""
    
                elif char2 == "{":
                    pass

                elif char2 == "}" and return_flag:
                    elements[1] = temp_word
                    temp_word = ""

                else:
                    temp_word += char2

            if temp_word != "":
                if elements[0] == "":
                    elements[0] = temp_word
                else:
                    elements[1] += temp_word

            # almacena en diccionario
            if elements[0] != "":
                self.tokens[(elements[0]).strip()] = (elements[1]).strip()

        print("\n",self.tokens,"\n")

    def expand_lets(self):
        # expandir los let en el diccionario de lets
        for key in self.lets:
            self.lets[key] = self.recursive_search(self.lets[key])
           

    def generate_regex(self):
        tokens_actualizados = []

        # recorrer tokens y generar expresiones regulares
        for key in self.tokens:

            # revisar si key tambien es un let
            if key in self.lets:
                tokens_actualizados.append(self.lets[key])

        
            

            

            






                

        