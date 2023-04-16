from set import Set

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
        with open(f"./scanner/{self.nameOutput}.py", "w") as archivo:
            if self.header != []:
                archivo.write("#-------- HEADER\n")
            for line in self.header:
                archivo.write(line+"\n")

    def generarTokens(self):
        with open(f"./scanner/{self.nameOutput}.py", "a") as archivo:
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

                archivo.write("\tif regla == '"+string_without_enter+"':\n")

                for line in temporal_tokens:
                    archivo.write("\t\t"+line+"\n")

    def generarSimulacion(self):
        pass

    def generarTrailer(self):
        with open(f"./scanner/{self.nameOutput}.py", "a") as archivo:
            if self.trailer != []:
                archivo.write("#-------- TRAILER\n")
            for line in self.trailer:
                archivo.write(line+"\n")
        

