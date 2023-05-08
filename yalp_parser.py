from simbolo import Simbolo
from transicion import Transicion
from automata import Automata
from estado import Estado
from prettytable import PrettyTable
from graphviz import Digraph
import numpy as np
import importlib
from yal_parser import YalParser
from set import Set

class YalPParser(Automata):
    def __init__(self, fileYalpar, fileYalex):

        # Inicializa la clase padre (Automata)
        super().__init__()

        print("\n-----")

        self.file = fileYalpar
        
        yal = YalParser(fileYalex)
        self.YalexTokens = yal.tokens

        # Contiene los caracteres que se pueden usar en la expresión regular
        self.charset = ["[", "]", "-"]
        self.define = ["(", ")"]
        self.operators = ["*", "+", "?", "|"]
        self.literal = ["'", '"']

        self.tokens = []
        self.productions = []

        self.parse()
        self.clean()

        self.lr0()

        self.first_calc()
        self.follow_calc()

        self.automaton()

        print("\n-----\n")

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

        # print("\BREAKPOINT - SEPARACION DE TOKENS Y PRODUCCIONES (DIRTY)")

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

                        
                if temporal_token == "%token" or temporal_token.lower() == "%token":
                    
                    if temporal_token != "%token":
                        print("\nError Lexico la linea", i+1, "de", self.file + ": Se esperaba que %token estuviera en minusculas.")

                    indicator = "token"
                    temporal_token = ""

                    if tokens_array[i][j+1] == " ":
                        continue
                    else:
                        print("\nError Lexico la linea", i+1, "de", self.file + ": Se esperaba un espacio después de %token.")
                        error_indicator = True

                elif temporal_token == "IGNORE":
                    indicator = "ignore"
                    temporal_token = ""

                    if tokens_array[i][j+1] == " ":
                        continue
                    else:
                        print("\nError Lexico la linea", i+1, "de", self.file + ": Se esperaba un espacio después de IGNORE.")
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
                        print("\nError Semantico la linea", i+1, "de", self.file + ": El token", token, "no ha sido declarado. No se puede 'IGNORE'.")

        for token_element in self.tokens:
            token_element[0] = token_element[0].upper()

        # print("\BREAKPOINT - TOKENS LIMPIOS")

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

        # print("\BREAKPOINT - PRODUCCIONES LIMPIAS")

        self.Simbolos.Elementos = ['ε']

        self.productionsOriginal = self.productions.copy()

        for production in self.productions:
            if production[0] not in self.Simbolos.Elementos:
                self.Simbolos.Elementos.append(production[0])

        for token in self.tokens:
            if token[0] not in self.Simbolos.Elementos:
                self.Simbolos.Elementos.append(token[0])

    def clean(self):
        to_delete = []
        new_Tokens = []

        for name, token in self.YalexTokens.items():
            new_name = ""

            for char in token:
                if char == '"' or char == "'":
                    continue
                elif char != " ":
                    new_name += char
                else:
                    new_name = ""

            new_Tokens.append(new_name)

        for token in self.tokens:
            if token[0] not in new_Tokens:
                print("\nError Semantico: El token", token[0], "encontrado en .Yalp no ha sido declarado en .Yalex. Ignorando...")
                to_delete.append(token)

        # for token in new_Tokens:
        #     found = False

        #     for element in self.tokens:
        #         if token == element[0]:
        #             found = True

        #     if found == False:
        #         print("Error Semantico: El token", token, "encontrado en .Yalex no ha sido declarado en .Yalp. Ignorando...")

        for token in to_delete:
            self.tokens.remove(token)   

        self.tokens.append(["ε", 0])

        to_delete = []
        for production in self.productions:
            words_found = set()

            temp_word = ""
            for char in production[1]:
                if char != " " and char != "|":
                    temp_word += char
                else:
                    words_found.add(temp_word)
                    temp_word = ""

            words_found.add(temp_word)
            temp_word = ""

            for word in words_found:

                if word.isupper() == True or not any(c.isalpha() for c in word):
                    found = False

                    for token in self.tokens:
                        if word == token[0]:
                            found = True
                            break

                    if found == False:
                        print("\nError Semantico: El token", word, "no ha sido declarado. Ignorando...")
                        to_delete.append(production)

                elif word.islower():
                    found = False

                    for symbol in self.Simbolos.Elementos:
                        if word == symbol:
                            found = True
                            break

                    if found == False:
                        print("\nError Semantico: El simbolo no terminal", word, "no ha sido declarado. Ignorando...")
                        to_delete.append(production)

                else:
                    print("\nError Semantico: El simbolo", word, "no ha sido declarado. Ignorando...")
                    to_delete.append(production)

        for production in to_delete:
            self.productions.remove(production)
            
        # print("\BREAKPOINT - DETECCION DE ERRORES")

    def lr0(self):
        inicial = self.productions[0][0]
        self.inicial_token = inicial
        self.productions.insert(0, [inicial+"'", inicial])
        self.end_item = [inicial+"'", inicial+' •']

        inicial = [0, [[inicial+"'", '• '+inicial]]]

        self.contador_item = 1
        self.transiciones = []
        C = [self.closure(inicial)]

        items = C[0][1:][0]
        number_items = C[0][2]
        items_preClosure = items[0:number_items]
        items_postClosure = items[number_items:]

        start = Estado(id=0, items_pre=items_preClosure, items_post=items_postClosure)
        self.Estados.AddItem(start)
        self.estado_inicial = start

        for i in C:
            for j in self.Simbolos.Elementos:
                goto = self.goto(i, j)

                items = goto[1:][0]
                number_items = goto[2]
                items_preClosure = items[0:number_items]
                items_postClosure = items[number_items:]

                if np.array_equal(np.array(goto[1], dtype=object), np.array([], dtype=object)) == False:

                    inside_C = False
                    found_item = None

                    for k in C:

                        if np.array_equal(np.array(goto[1:][0], dtype=object), np.array(k[1:][0], dtype=object)) == True:
                            inside_C = True
                            found_item = k[0]

                    if inside_C == False:
                        C.append(goto)
                        self.Estados.AddItem(Estado(id=goto[0], items_pre=items_preClosure, items_post=items_postClosure))
                        self.transiciones.append(Transicion(i[0], self.contador_item,  j))
                        self.contador_item += 1
                    else:
                        self.transiciones.append(Transicion(i[0], found_item,  j))

        found = False
        for element in self.Estados.Elementos:
            if found == True:
                break

            for item in element.items_pre:
                if item[1] == self.end_item[1]:
                    self.transiciones.append(Transicion(element.id, "Aceptar", "$"))
                    last = Estado(id="Aceptar")
                    self.Estados.AddItem(last)
                    self.EstadosFinales.AddItem(last)
                    found = True
                    break

        # print("\BREAKPOINT - LR0")

    def closure(self, I):
        id_item = I[0]
        J = I[1:][0]

        size_preclosure = len(J)

        analized = []

        for item in J:

            current_prod = item[1].split(" ")
            index = current_prod.index("•")

            if index+1 >= len(current_prod):
                continue

            if current_prod[index+1] in self.tokens:
                continue

            to_analize = current_prod[current_prod.index("•")+1]
        
            for prod in self.productions:

                if prod[0] == to_analize:
                    if prod[0] not in analized:
                        current_prod_copy = [to_analize, "• "+prod[1]]
                        J.append(current_prod_copy)

            analized.append(to_analize)

        return [id_item, J, size_preclosure]

    def goto(self, I, X):

        new_Items = [self.contador_item, []]
        I = I[1:][0]
        
        for I_item in I:
            current_prod = I_item[1].split(" ")
            index = current_prod.index("•")

            if index+1 >= len(current_prod):
                continue

            to_analize = current_prod[current_prod.index("•")+1]

            if to_analize == X:
                current_prod_copy = current_prod.copy()
                index = current_prod_copy.index("•")
                
                current_prod_copy.insert(index+2, "•")
                current_prod_copy.pop(index)

                current_prod_copy = " ".join(current_prod_copy)

                new_Items[1].append([I_item[0],current_prod_copy])

        return self.closure(new_Items)


    def first_calc(self):
            
        production_copy = self.productionsOriginal.copy()

        for production in production_copy:

            name_prod = production[0]
            prod = production[1].split(" ")

            for token in self.tokens:
                if prod[0] == token[0]:
                    if self.first == {}:
                        self.first[name_prod] = [prod[0]]
                    else:
                        if name_prod in self.first.keys():
                            elements = self.first[name_prod]
                            if prod[0] not in elements:
                                self.first[name_prod].append(prod[0])
                        else:
                            self.first[name_prod] = [prod[0]]
                        

            same_prod = Set()
            same_prod.AddItem(name_prod)
            same_prod.AddItem(prod[0])

            for prod2 in production_copy:
                if prod2[0] == same_prod.returnLastItem():
                    result = prod2[1].split(" ")[0]

                    reached = False
                    for token in self.tokens:
                        if result == token[0]:

                            for item in same_prod.Elementos:

                                if self.first == {}:
                                    self.first[item] = [result]
                                else:
                                    if item in self.first.keys():
                                        elements = self.first[item]
                                        if result not in elements:
                                            self.first[item].append(result)
                                    else:
                                        self.first[item] = [result]
                                        
                                    
                                reached = True

                    if reached == False:
                        same_prod.AddItem(result)
            
        print(self.first)

    def follow_calc(self):
        self.follow[self.inicial_token] = ["$"]

        non_terminals = []
        for production in self.productionsOriginal:
            non_terminals.append(production[0])

        for production in self.productionsOriginal:

            prod_original = production[0]
            prod = production[1].split(" ")

            for i in range(len(prod)):

                # check if there is a non-terminal surrounded by non-terminals on both sides
                if i+1 < len(prod) and i-1 >= 0 and prod[i-1] in non_terminals and prod[i] in non_terminals and prod[i+1] in non_terminals:

                    firstB = self.first[prod[i+1]]
                    for item in firstB:
                        if item == 'ε':
                            # delete epsilon
                            firstB.remove(item)

                    if prod[i] in self.follow.keys():
                        for item in firstB:
                            if item not in self.follow[prod[i]]:
                                self.follow[prod[i]].append(item)
                    else:
                        self.follow[prod[i]] = firstB


        for production in self.productionsOriginal:

            prod_original = production[0]
            prod = production[1].split(" ")

            for i in range(len(prod)):

                # check if there is a non-terminal surrounded by
                if i+1 < len(prod) and i-1 >= 0 and prod[i-1] in non_terminals and prod[i] in non_terminals and prod[i+1] in non_terminals:
                    firstB = self.first[prod[i+1]]
                    epsilon_check = False
                    for item in firstB:
                        if item == 'ε':
                            epsilon_check = True

                    if epsilon_check == True:
                        if prod[i] in self.follow.keys() and prod_original in self.follow.keys():
                            for item in self.follow[prod_original]:
                                if item not in self.follow[prod[i]]:
                                    self.follow[prod[i]].append(item)
                        elif prod[i] not in self.follow.keys() and prod_original in self.follow.keys():
                            self.follow[prod[i]] = self.follow[prod_original]

                        else:
                            self.follow[prod[i]] = []

                elif i+1 > len(prod) and i-1 >= 0 and prod[i-1] in non_terminals and prod[i] in non_terminals:
                    if prod[i] in self.follow.keys() and prod_original in self.follow.keys():
                        for item in self.follow[prod_original]:
                            if item not in self.follow[prod[i]]:
                                self.follow[prod[i]].append(item)
                    elif prod[i] not in self.follow.keys() and prod_original in self.follow.keys():
                        self.follow[prod[i]] = self.follow[prod_original]

                    else:
                        self.follow[prod[i]] = []

        print(self.follow)

    def automaton(self):
        dot = Digraph()
        dot.attr(rankdir="LR")

        dot.attr(fontsize='20')
        nodes_array = []
    
        for C in self.Estados.Elementos:
            id = C.id
            items_preClosure = C.items_pre
            items_postClosure = C.items_post

            if id == "Aceptar":
                continue

            # Create box styled nodes. Each node should include ID in red, items_preClosure in blue and items_postClosure in green
            node = "i"+str(id)
            node += "\n-----------\n"
            for item in items_preClosure:
                node += item[0] + " => " +item[1] + "\n"
            node += "-----------\n"
            for item in items_postClosure:
                node += item[0] + " => " +item[1] + "\n"

            nodes_array.append([id, node])

        for transition in self.transiciones:
            origin = transition.estado_origen
            destination = transition.estado_destino

            for node in nodes_array:
                if node[0] == origin:
                    origin = node[1]
                if node[0] == destination:
                    destination = node[1]

            dot.edge(str(origin), str(destination), transition.el_simbolo)

        # Render graph
        dot.node_attr.update({'shape': 'box'})
        dot.render(view=True, format='pdf')



YalParser = YalPParser("./yalex/slr-1.yalp", "./yalex/slr-1.yal")