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

    def generarHeader(self):
        with open(f"{self.nameOutput}.py", "w") as archivo:
            archivo.write("import pickle\n")
            archivo.write("from simulacion import Simulacion\n")
            archivo.write("from prettytable import PrettyTable\n")
            archivo.write("from afd_directo import AFD_Directo\n")
            if self.header != []:
                archivo.write("#-------- HEADER\n")
            for line in self.header:
                archivo.write(line+"\n")

            archivo.write("\n\n#-------- TOKENS\n")

    def generarTokens(self):
        with open(f"{self.nameOutput}.py", "a") as archivo:
            archivo.write("def tokens(regla, token):\n")
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

                archivo.write("\tif regla.replace(\"'\", \"\").replace('\"', \"\") == '"+token.replace("'",'').replace('"', "")+"':\n")

                for line in temporal_tokens:
                    archivo.write("\t\t"+line+"\n")
            
            archivo.write("\telse:\n")
            archivo.write("\t\treturn 'Error: Token no definido!'\n\n")

    def generarSimulacion(self):
        serialized_object = pickle.dumps(self.afd_directo)

        with open(f"{self.nameOutput}.py", "a") as archivo:
            archivo.write("\n#-------- SIMULACION\n")
            archivo.write("def simulacion():\n")

        # Save the serialized object to a file
        with open(f"./scanner/{self.nameOutput}.pkl", "wb") as file:
            file.write(serialized_object)

        with open(f"{self.nameOutput}.py", "a") as archivo:
            archivo.write(f"\twith open(f'./scanner/{self.nameOutput}.pkl', 'rb') as file:\n")
            archivo.write("\t\tserialized_object = file.read()\n\n")
            archivo.write("\tautomata = pickle.loads(serialized_object)\n")
            archivo.write("\tresultado = None\n\n")

            archivo.write("\twith open('./yalex/prueba.txt', 'r') as archivo:\n")
            archivo.write("\t\tcontenido = archivo.read()\n\n")

            archivo.write("\tresultado = Simulacion(automata, contenido, 'Yalex').resultado\n")

            archivo.write("\tfor res in resultado:\n")
            archivo.write("\t\tres_token = tokens(res[0], res[1])\n")
            archivo.write("\t\tres.append(res_token)\n\n")

            archivo.write("\ttable = PrettyTable()\n")
            archivo.write("\ttable.field_names = [\"TOKEN\", \"VALUE\",\"RESULT\"]\n")
            archivo.write("\tfor res in resultado:\n")
            archivo.write("\t\ttable.add_row([res[0], res[1], res[2]])\n")
            archivo.write("\tprint(table)\n")

            if self.trailer != []:
                archivo.write("\n\t#-------- TRAILER\n")
            for line in self.trailer:
                archivo.write("\t"+line+"\n")

            archivo.write("\n\treturn resultado\n")

            archivo.write("\nsimulacion()\n")


        

