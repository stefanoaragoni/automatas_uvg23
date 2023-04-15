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
            token_completo = ""
            start_end_token = [0,0]

            # revisar a que corresponde cada linea
            for line in file:
                line = line.strip()

                starting_with = ""
                for char in line:
                    if char == " ":
                        break
                    else:
                        starting_with += char

                if line == "":
                    pass

                # let = | se agrega a let_array
                elif starting_with.startswith("let"):
                    contenido_to_store = ""
                    let_name = ""
                    first_space = False

                    for i, char in enumerate(line):
                        if char == " " and not first_space:
                            first_space = True

                        if first_space:
                            contenido_to_store += char
                        else:
                            let_name += char

                    if let_name.upper() == "LET":
                        pass
                    else:
                        print(f"\nDeteccion Error: Se encontro un error en la declaracion de let: {line}.")

                    let_array.append((contenido_to_store).strip())
                
                # rule = | se activa rules
                elif starting_with.startswith("rule"):
                    if starting_with.upper() == "RULE":
                        pass
                    else:
                        print(f"\nDeteccion Error: Se encontro un error en la declaracion de rule: {line}.")
                    rules = True

                # tokens = | se agrega a tokens_array
                elif rules:

                    if "{" not in line and start_end_token[0] == 0 and start_end_token[1] == 0:
                        tokens_array.append(line.strip())

                    else:
                        for i, char in enumerate(line.strip()):
                            if i == 0:
                                token_completo += " "

                            if char == "}" or char == "{":
                                start_end_token[0] += 1
                                start_end_token[1] += 1

                                if start_end_token[0] == 2 and start_end_token[1] == 2:
                                    start_end_token[0] = 0

                            if i == len(line)-1 and start_end_token[0] == 0 and start_end_token[1] == 2:
                                token_completo += char
                                tokens_array.append(token_completo)
                                token_completo = ""
                                start_end_token[0] = 0
                                start_end_token[1] = 0
                            
                            else:
                                token_completo += char

        
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

            comillas = 0
            contenido_sin_espacios = ""

            for char in new_line[1]:
                if char == "'" or char == '"':
                    comillas = comillas + 1
                    if comillas == 2:
                        comillas = 0
                
                if char == " " and comillas == 0:
                    pass
                else:
                    contenido_sin_espacios += char

            # almacena en diccionario
            self.lets[new_line[0]] = contenido_sin_espacios

        # Limpieza de tokens_array.
        # Resultado deseado: {token: 'return X'}"}}
        for i in range(len(tokens_array)):
            current_line = tokens_array[i].strip()
            new_line = ""

            comillas = 0
            comentario = 0

            for i, char in enumerate(current_line):

                if char == "'" or char == '"':
                    comillas = comillas + 1
                    if comillas == 2:
                        comillas = 0
                
                # elimina comentarios
                if i+1 < len(current_line):
                    if char == "(" and current_line[i+1] == "*" and comillas == 0:
                        comentario = 2

                    elif char == "*" and current_line[i+1] == ")" and comillas == 0:
                        comentario = comentario - 1

                # elimina comentarios
                comment_ended = False
                if i-1 >= 0:
                    if char == ")" and current_line[i-1] == "*" and  comillas == 0:
                        comentario = comentario - 1
                        comment_ended = True

                # elimina comentarios
                if comentario == 0 and not comment_ended:
                    if (char == '|' and i == 0):
                        pass
                    else:
                        new_line += char

            # verifica que comentario no este abierto
            if comentario != 0:
                print("\nError: comentario no cerrado. Saltando linea: '", current_line)
            else:
                new_line = new_line.strip()

                elements = ["",""]

                temp_word = ""
                return_flag = False

                # separa contenido en nombre y contenido
                for char2 in new_line:
                    
                    if char2 == " " and not return_flag:
                        if temp_word != "":
                            elements[0] = temp_word
                            temp_word = ""
        
                    elif char2 == "{":
                        temp_word = ""
                        return_flag = True
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
        error_ = []

        for key in self.lets:

            charset_flag = False
            define_flag = False
            special_char = False
            contenido_array = []

            new_line = ""

            for char_id, char in enumerate(self.lets[key]):
                # elimina linea en caso no se tenga el charset completo
                if charset_flag and char_id == len(self.lets[key])-1 and char != "]":
                    print("Error: '[' sin ']'. Agregando ']' en",key,": ", self.lets[key])
                    char = "]"

                if char == "[":
                    charset_flag = True

                elif char == "]":
                    if charset_flag:
                        charset_flag = False
                    
                    # En caso haya ] pero nunca haya [
                    else:
                        print("\nError: ']' sin '['. Saltando",key,": ", self.lets[key])
                        error_.append(key)
                        break

                    updated_contenido_array = []

                    for i in range(len(contenido_array)):

                        if contenido_array[i] == "-":
                            if i+1 < len(contenido_array):
                                # generar la secuencia de caracteres de i-1 a 1+1
                                for j in range(contenido_array[i-1], contenido_array[i+1]+1):
                                    # convertir ascci a caracter y agregarlo a updated_contenido_array
                                    #updated_contenido_array.append(chr(j))
                                    updated_contenido_array.append("'"+str(j)+"'")

                    if len(updated_contenido_array) == 0:
                        for contenido in contenido_array:
                            if chr(contenido) == '\t' or chr(contenido) == '\n' or chr(contenido) == '\r' or chr(contenido) == '\f' or chr(contenido) == ' ' or chr(contenido) in self.operators or chr(contenido) in self.define:
                                updated_contenido_array.append("'"+str(contenido)+"'")

                            else:
                                #updated_contenido_array.append(chr(contenido))
                                updated_contenido_array.append("'"+str(contenido)+"'")

                    # separar updated_contenido_array por "|" y pasar a string
                    updated_contenido_array = "|".join(updated_contenido_array)
                    new_line += "("+updated_contenido_array+")"

                    contenido_array = []
                    updated_contenido_array = []

                elif (char == "'") or (char == '"'):
                    define_flag = not define_flag

                elif not charset_flag and define_flag:
                    new_line += "'"+str(ord(char))+"'"

                elif not charset_flag and not define_flag:
                    if not char.isalpha() and not char.isnumeric() and char not in self.charset and char not in self.define and char not in self.operators:
                        new_line += "'"+str(ord(char))+"'"
                    else:
                        new_line += char

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
                        else:
                            print("\nError: Se ingresó secuencia de escape invalida. Saltando linea: '", self.lets[key])
                        special_char = False
                    else:
                        contenido_array.append(ord(char))

            correcto_or_error = self.verify_regex(new_line)

            if correcto_or_error:
                error_.append(key)
            else:
                self.lets[key] = new_line

        for element in error_:
            self.lets.pop(element)

        #print(self.lets)
        
    def generate_regex(self):
        # remplaza en los lets las llaves por su contenido
        updated_content = self.replace_keys(self.lets)

        # remplaza los tokens por su contenido y crea la regex
        self.regex = []

        for key in self.tokens:
            value = "'#"+self.tokens[key]+"'"

            if key in updated_content.keys():
                temporal_regex = "(("+updated_content[key]+")"+value+")"
                self.regex.append(temporal_regex)

            else:
                if "'" in key or '"' in key:
                    key_without_apostrophe = key.replace('"', "")
                    key_without_apostrophe = key_without_apostrophe = key.replace("'", "").replace('"', "")

                    if len(key_without_apostrophe) > 1:
                        
                        temporal_regex = []

                        for char in key_without_apostrophe:
                            temporal_regex.append("'"+str(ord(char))+"'")

                        temporal_regex = "("+("".join(temporal_regex))+")"
                        temporal_regex = "("+temporal_regex+value+")"

                        self.regex.append(temporal_regex)

                    else:
                        temporal_regex = "(("+"'"+str(ord(key_without_apostrophe))+"'"+")"+value+")"
                        self.regex.append(temporal_regex)

                else:
                    print("\nError: Token ID ('"+key+"') no encontrado den el diccionario de 'let'. Saltando linea. \n")

        self.regex = "|".join(self.regex)

    def replace_keys(self, patterns):
        to_delete = []

        for k, v in patterns.items():

            word_found = ""
            define_flag = False
            new_value = ""

            # recorrer v en busqueda de palabras.
            for char in v:

                # si el char es una letra, agregarlo a la palabra de lookup
                if char.isalpha() and not define_flag:
                    word_found += char

                # si el char no es una letra, agregar la palabra a la lista
                else:
                    # si el char es un define, cambiar bandera
                    if char == "'" or char == '"':
                        define_flag = not define_flag

                    if word_found != "" and word_found in patterns.keys():
                        new_value += patterns[word_found]
                        new_value += char
                        word_found = ""

                    elif word_found != "" and word_found not in patterns.keys():
                        print("\nError: Keyword ('"+word_found+"') no encontrada en el diccionario de 'let'. Saltando linea: ",k,":", v)
                        to_delete.append(k)
                        new_value = ""
                        break

                    else:
                        new_value += char
                        word_found = ""

            patterns[k] = new_value
        
        for element in to_delete:
            patterns.pop(element)

        return patterns

    # Verifica que la expresión regular infix sea válida; si no lo es, lanza una excepción
    def verify_regex(self, regex):
        error = False # bandera para indicar si hubo un error

        if regex == '':
            print('\nError: La linea no puede estar vacía.\n')
            error = True
            return error
        if regex[0] in self.operators:
            print('\nError: El let no puede iniciar con un operador: ',regex)
            error = True
            return error

        simbolos_binarios = ['|', '•']
        simbolos_unarios = ['*', '+', '?']
        for i, char in enumerate(regex):
            if i+1 < len(regex):
                
                if char in simbolos_binarios and regex[i+1] in simbolos_binarios:
                    print('\nError: El let no puede tener dos operadores seguidos como "|": ',regex)
                    error = True
                    break
                
                if char in simbolos_binarios and regex[i+1] == ')':
                    print('\nError: El let no puede tener un operador binario seguido de un paréntesis de cierre: ',regex)
                    error = True
                    break

                if (char == '(' and regex[i+1] in simbolos_unarios) or (char == '(' and regex[i+1] in simbolos_binarios):
                    print('\nError: El let no puede tener un paréntesis de apertura seguido de un operador: ',regex)
                    error = True
                    break

                if (char == '(' and regex[i+1] == ')'):
                    print('\nError: El let no puede tener un paréntesis de apertura seguido de un paréntesis de cierre.: ',regex)
                    error = True
                    break

                if char in simbolos_binarios and regex[i+1] in simbolos_unarios:
                    print('\nError: El let no puede tener un operador binario seguido de un operador unario como "*", "+", "?": ',regex)
                    error = True
                    break

        if regex[-1] in ['|']:
            print('\nError: El let no puede terminar con un operador como "|": ',regex)
            error = True
            
        if regex.count('(') != regex.count(')'):
            print('\nError: Los paréntesis no están balanceados: ',regex)
            error = True

        return error

            

            






                

        