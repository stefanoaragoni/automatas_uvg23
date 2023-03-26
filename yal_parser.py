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

        #print("\n",self.tokens,"\n")

    def expand_lets(self):
        # expandir los let en el diccionario de lets
        for key in self.lets:

            charset_flag = False
            define_flag = False

            special_char = False

            contenido_array = []

            new_line = ""

            for char in self.lets[key]:
                if char == "[":
                    charset_flag = True

                elif char == "]":
                    charset_flag = False

                    updated_contenido_array = []

                    for i in range(len(contenido_array)):

                        if contenido_array[i] == "-":
                            if i+1 < len(contenido_array):
                                # generar la secuencia de caracteres de i-1 a 1+1
                                for j in range(contenido_array[i-1], contenido_array[i+1]+1):
                                    # convertir ascci a caracter y agregarlo a updated_contenido_array
                                    updated_contenido_array.append(chr(j))

                    if len(updated_contenido_array) == 0:
                        for contenido in contenido_array:
                            if chr(contenido) == '\t' or chr(contenido) == '\n' or chr(contenido) == '\r' or chr(contenido) == '\f' or chr(contenido) == ' ' or chr(contenido) in self.operators or chr(contenido) in self.define:
                                updated_contenido_array.append("'"+str(contenido)+"'")

                            else:
                                updated_contenido_array.append(chr(contenido))

                    # separar updated_contenido_array por "|" y pasar a string
                    updated_contenido_array = "|".join(updated_contenido_array)
                    new_line += "("+updated_contenido_array+")"

                    contenido_array = []
                    updated_contenido_array = []

                elif not charset_flag and not define_flag:
                    new_line += char

                elif (char == "'" and charset_flag) or (char == '"' and charset_flag):
                    define_flag = not define_flag

                elif char == "-" and charset_flag and not define_flag:
                    contenido_array.append("-")
                
                elif char == "-" and charset_flag and define_flag:
                    contenido_array.append(ord("-"))

                elif charset_flag and define_flag:
                    if char == "\\":
                        special_char = True
                    elif special_char:
                        if char == "n":
                            contenido_array.append(ord("\n"))
                        elif char == "t":
                            contenido_array.append(ord("\t"))
                        elif char == "r":
                            contenido_array.append(ord("\r"))
                        elif char == "f":
                            contenido_array.append(ord("\f"))
                        elif char == "s":
                            contenido_array.append(ord(" "))
                        special_char = False
                    else:
                        contenido_array.append(ord(char))

            self.lets[key] = new_line

        #print(self.lets)
        
    def generate_regex(self):
        # remplaza en los lets las llaves por su contenido
        updated_content = self.replace_keys(self.lets)

        # remplaza los tokens por su contenido y crea la regex
        self.regex = []

        for key in self.tokens:

            if key in updated_content.keys():
                self.regex.append(updated_content[key])

            else:
                key_without_apostrophe = key.replace('"', "")
                key_without_apostrophe = key_without_apostrophe = key.replace("'", "").replace('"', "")

                if len(key_without_apostrophe) > 1:
                    self.regex.append("'"+key_without_apostrophe+"'")
                elif key_without_apostrophe not in self.define and key_without_apostrophe not in self.operators:
                    self.regex.append(key_without_apostrophe)
                else:
                    self.regex.append("'"+str(ord(key_without_apostrophe))+"'")

        self.regex = "|".join(self.regex)

        print(self.regex)

    def replace_keys(self, patterns):
        for k, v in patterns.items():
            if isinstance(v, str):
                for inner_k in patterns.keys():
                    if inner_k in v:
                        
                        word_found = ""
                        # recorrer v en busqueda de palabras.
                        for char in v:

                            if char == " " or char == "(" or char == ")" or char == "[" or char == "]" or char == "{" or char == "}" or char == "|" or char == "*" or char == "+" or char == "?" or char == "." or char == "^" or char == "$" or char == "\\" or char == "'" or char == '"':
                                # si la palabra no esta vacia, agregarla a la lista
                                if word_found != "":
                                    if word_found in patterns.keys():
                                        patterns[k] = patterns[k].replace(word_found, patterns[word_found])
                                    word_found = ""
                            # si el caracter no un espacio o simbolo, agregar la palabra a la lista
                            else:
                                word_found += char

            elif isinstance(v, dict):
                patterns[k] = self.replace_keys(v)

        return patterns

        
            

            

            






                

        