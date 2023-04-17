from set import Set
import pickle

class scannerGenerator:
    def __init__(self, afd_directo, header, trailer, tokens, nameOutput):
        self.afd_directo = afd_directo
        self.header = header
        self.trailer = trailer
        self.tokens = tokens
        self.nameOutput = nameOutput
        self.generarScanner()

    def generarScanner(self):
        self.generarHeader()
        self.generarTokens()
        self.generarSimulacion()
        self.generarTrailer()

    def generarHeader(self):
        with open(f"{self.nameOutput}.py", "w") as archivo:
            archivo.write("import pickle\n")
            archivo.write("from prettytable import PrettyTable\n")
            archivo.write("from afd_directo import AFD_Directo\n")
            if self.header != []:
                archivo.write("#-------- HEADER\n")
            for line in self.header:
                archivo.write(line+"\n")

    def generarTokens(self):
        with open(f"{self.nameOutput}.py", "a") as archivo:
            archivo.write("def tokens(token, regla):\n")
            for token in self.tokens:

                temporal_tokens = []
                temporal_string = ""

                for char in self.tokens[token]:
                    if char == '\n':
                        temporal_tokens.append(temporal_string)
                        temporal_string = ""
                    else:
                        temporal_string += char

                if temporal_string != "":
                    temporal_tokens.append(temporal_string)

                string_without_enter = ""
                for line in temporal_tokens:
                    string_without_enter += line + " "

                string_without_enter = string_without_enter.strip()

                archivo.write("\tif regla == '"+token.replace("'","")+"':\n")

                for line in temporal_tokens:
                    archivo.write("\t\t"+line+"\n")

    def generarSimulacion(self):
        serialized_object = pickle.dumps(self.afd_directo)

        # Save the serialized object to a file
        with open(f"./scanner/{self.nameOutput}.pkl", "wb") as file:
            file.write(serialized_object)

        with open(f"{self.nameOutput}.py", "a") as archivo:
            archivo.write("\n#-------- SIMULACION\n")
            archivo.write(f"with open(f'./scanner/{self.nameOutput}.pkl', 'rb') as file:\n")
            archivo.write("\tserialized_object = file.read()\n\n")
            archivo.write("automata = pickle.loads(serialized_object)\n")
            archivo.write("resultado = None\n\n")

            archivo.write("def simularAFD(estado, cadena):\n\n")
            archivo.write("\tglobal automata\n")
            archivo.write("\tglobal resultado\n\n")
            archivo.write("\tif len(cadena) != 0:\n")
            archivo.write("\t\tfor transicion in automata.transiciones:\n")
            archivo.write("\t\t\tif transicion.estado_origen == estado and transicion.el_simbolo.id.replace(\"'\", \"\") == str(ord(cadena[0])):\n")
            archivo.write("\t\t\t\tsimularAFD(transicion.estado_destino, cadena[1:])\n")
            archivo.write("\tif len(cadena) == 0:\n")
            archivo.write("\t\tresultado = estado\n")
            archivo.write("\t\treturn\n\n")

            archivo.write("def simularAFD_Yalex(estado, cadena):\n\n")
            archivo.write("\tglobal automata\n")
            archivo.write("\tglobal resultado\n")
            archivo.write("\tcurrent_state = estado\n")
            archivo.write("\tlast_result = None\n")
            archivo.write("\tchar_set = []\n")
            archivo.write("\tresultado2 = []\n")
            archivo.write("\tresult_token = None\n\n")
            archivo.write("\tfor i, char in enumerate(cadena):\n\n")
            archivo.write("\t\tsimularAFD(current_state, char)\n\n")
            archivo.write("\t\twhile True:\n")
            archivo.write("\t\t\tif resultado:\n")
            archivo.write("\t\t\t\tcurrent_state = resultado\n")
            archivo.write("\t\t\t\tchar_set.append(char)\n")
            archivo.write("\t\t\t\tresultado = None\n")
            archivo.write("\t\t\t\tlast_result = True\n\n")
            archivo.write("\t\t\t\tif i == len(cadena) - 1:\n")
            archivo.write("\t\t\t\t\ttoken = ''.join(char_set)\n")
            archivo.write("\t\t\t\t\ttemp_token = (current_state.token.id).replace(\"'\", \"\").replace('\"', \"'\").replace(\"#\", \"\")\n")
            archivo.write("\t\t\t\t\tresult_token = tokens(token, temp_token)\n")
            archivo.write("\t\t\t\t\tresultado2.append([result_token, token])\n\n")
            archivo.write("\t\t\t\tbreak\n\n")
            archivo.write("\t\t\telif last_result and resultado == None:\n")
            archivo.write("\t\t\t\ttoken = ''.join(char_set)\n")
            archivo.write("\t\t\t\ttemp_token = (current_state.token.id).replace(\"'\", \"\").replace('\"', \"'\").replace(\"#\", \"\")\n")
            archivo.write("\t\t\t\tresult_token = tokens(token, temp_token)\n")
            archivo.write("\t\t\t\tresultado2.append([result_token, token])\n\n")
            archivo.write("\t\t\t\tcurrent_state = estado\n")
            archivo.write("\t\t\t\tchar_set = []\n")
            archivo.write("\t\t\t\tlast_result = False\n\n")
            archivo.write("\t\t\t\tsimularAFD(current_state, char)\n\n")
            archivo.write("\t\t\telse:\n")
            archivo.write("\t\t\t\tresultado2.append([\"Error Lexico\", char])\n")
            archivo.write("\t\t\t\tbreak\n\n")

            archivo.write("\treturn resultado2\n\n")

            # with open("./yalex/prueba.txt", "r") as archivo:
            #    contenido = archivo.read()

            archivo.write("with open('./yalex/prueba.txt', 'r') as archivo:\n")
            archivo.write("\tcontenido = archivo.read()\n\n")

            archivo.write("resultado2 = simularAFD_Yalex(automata.estado_inicial, contenido)\n\n")

            archivo.write("table = PrettyTable()\n")
            archivo.write("table.field_names = [\"TOKEN\", \"VALUE\"]\n")
            archivo.write("for res in resultado2:\n")
            archivo.write("\ttable.add_row([res[0], res[1]])\n")
            archivo.write("print(table)\n")



    def generarTrailer(self):
        with open(f"{self.nameOutput}.py", "a") as archivo:
            if self.trailer != []:
                archivo.write("#-------- TRAILER\n")
            for line in self.trailer:
                archivo.write(line+"\n")
        

