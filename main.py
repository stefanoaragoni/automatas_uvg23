from set import Set
from estado import Estado
from simbolo import Simbolo
from transicion import Transicion
from automata import Automata
from afd_directo import AFD_Directo
from postfix import Postfix
from arbol import Arbol
from graph import Graph
from scanner_generator import scannerGenerator
from yal_parser import YalParser
from yalp_parser import YalPParser
from simulacion import Simulacion
from prettytable import PrettyTable

def main():

    with open("./yalex/prueba.txt", "r") as archivo:
        contenido = archivo.read()

    yal_file = ["slr-1.yal", "slr-3.yal", "lab-f.yal"]
    yalp_file = ["slr-1.yalp", "slr-3.yalp", "lab-f.yalp"]
    opcion = 0

    while True:
        print("\nArchivos Yalex:")
        for i in range(len(yal_file)):
            print(f"\t{i+1}. {yal_file[i]}")

        opcion = int(input("\nIngrese el número del archivo Yalex a evaluar: "))
        print("\n")
        
        if opcion > 0 and opcion <= len(yal_file):
            yal = YalParser("./yalex/"+yal_file[opcion-1])
            postfix_expr = Postfix(yal.regex)

            header = yal.header
            trailer = yal.trailer
            tokens = yal.tokens

            if postfix_expr.error:
                print("\nExpresión Regular inválida!") 
                opcion = 0
                input("\nPresione ENTER para continuar...")

            else:
                print("-----\nExpresión Regular (infix):\n",postfix_expr.regex)
                print("-----\nExpresión Regular (postfix):\n",postfix_expr.postfix)

                tree = Arbol(postfix_expr.postfix)
                tree.print_tree("Yalex Tree")

                afd_directo = AFD_Directo(tree)
                Graph(afd_directo, postfix_expr.regex.replace("'",""), "AFD_Directo")
                scannerGenerator(afd_directo, header, trailer, tokens, yal_file[opcion-1].replace(".yal",""))

                # namespace = {}
                # filename = yal_file[opcion-1].replace(".yal",".py")
                # with open(filename, 'r') as file:
                #     code = file.read()

                # exec(code, namespace)
                # result = namespace['result']
                # print(result)


                # -------- Según las instrucciones:
                # Este deberá tomar como entrada una gramática que defina a un lenguaje regular, 
                # siguiendo la sintaxis correcta de un archivo en lenguaje YAPar. 

                # Asimismo, tomará como entrada también los tokens de la previa ejecución de su 
                # Generador de Analizadores Léxicos,YALex
                yalp = YalPParser("./yalex/"+yalp_file[opcion-1], tokens)
                yalp.generate_parser()

                opcion = 0
                input("\nPresione ENTER para continuar...")
        
        else:
            print("\nOpción inválida.")
            break

if __name__ == "__main__":
    main()