'''
    Arbol de expresiones regulares generado a partir de una expresión regular en postfix.
        Cada nodo del árbol es una instancia de la clase Nodo.
            Cada nodo tiene un valor, y puede tener un hijo izquierdo y un hijo derecho.
            Si el nodo es una hoja, entonces no tiene hijos.
            Si el nodo es un operador, entonces tiene hijo(s). 
                Si el nodo es un operador unario, entonces tiene un hijo.
                    Si el nodo es un operador unario, entonces el hijo es el nodo izquierdo.
                Si el nodo es un operador binario, entonces tiene dos hijos.
                    Si el nodo es un operador binario, entonces el hijo izquierdo es el primer hijo.
                    Si el nodo es un operador binario, entonces el hijo derecho es el segundo hijo.
'''
class Arbol:
    # Constructor
    def __init__(self, regex):
        self.operators = ['|', '.', '*', '+', '?']
        self.operator_precedence = {'|': 1, '.': 2, '*': 3, '+': 3, '?': 3}
        self.regex = regex

        self.root = self.construct_tree()

    # Construye el árbol de expresiones regulares
    def construct_tree(self):
        stack = []

        # Recorre la expresión regular en postfix
        for char in self.regex:
            if char in self.operators:
                if char == '|':
                    right = stack.pop()
                    left = stack.pop()
                    node = Nodo('|', left, right)
                elif char == '.':
                    right = stack.pop()
                    left = stack.pop()
                    node = Nodo('.', left, right)
                elif char == '*':
                    child = stack.pop()
                    node = Nodo('*', child)
                elif char == '+' or char == '?':
                    child = stack.pop()
                    node = Nodo('|', child, Nodo('ε'))
                stack.append(node)
            else:
                node = Nodo(char)
                stack.append(node)
        
        # Retorna la raíz del árbol
        return stack.pop()
        
    def print_tree(self, nodo, prefix):
        print(nodo.valor)
        if nodo.izq:
            print(prefix + '├── ', end='')
            self.print_tree(nodo.izq, prefix + '│   ')
        if nodo.der:
            print(prefix + '└── ', end='')
            self.print_tree(nodo.der, prefix + '    ')

'''
    Clase Nodo almacena el valor de un nodo del árbol de expresiones regulares.
'''
class Nodo:
    def __init__(self, valor, izq=None, der=None):
        self.valor = valor
        self.izq = izq
        self.der = der