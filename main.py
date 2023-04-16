from set import Set
from estado import Estado
from simbolo import Simbolo
from transicion import Transicion
from automata import Automata
from afn import AFN
from afd_subconjuntos import AFD_Subconjuntos
from afd_directo import AFD_Directo
from afd_minimizacion import AFD_Minimizacion
from postfix import Postfix
from arbol import Arbol
from graph import Graph
from yal_parser import YalParser
from simulacion import Simulacion
from prettytable import PrettyTable

def main():

    with open("./yalex/prueba.txt", "r") as archivo:
        contenido = archivo.read()

    yal_file = ["slr-0.yal", "slr-1.yal", "slr-2.yal", "slr-3.yal", "slr-4.yal"]
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

                print("\nSimulacion:")
                resultados = Simulacion(afd_directo, contenido, 'Yalex', header, trailer).resultado

                table = PrettyTable()
                table.field_names = ["TOKEN", "VALUE"]
                for resultado in resultados:
                    table.add_row([resultado[0], resultado[1]])
                print(table)

                opcion = 0
                input("\nPresione ENTER para continuar...")
        
        else:
            print("\nOpción inválida.")
            break

if __name__ == "__main__":
    main()