from simbolo import Simbolo
import uuid
from graphviz import Digraph

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
                elif char == '+':
                    child = stack.pop()
                    node = Nodo('.', child, Nodo('*' , child))
                elif char == '?':
                    child = stack.pop()
                    node = Nodo('|', child, Nodo('ε'))
                stack.append(node)
            else:
                node = Nodo(char)
                stack.append(node)
            
        # Retorna la raíz del árbol
        return stack.pop()

        
    def print_tree(self, regex):
        # Implementacion de Graphviz
        dot = Digraph()

        # Añade los nodos al grafo
        self.add_node(dot, self.root)

        dot.attr(label=regex)

        # Exporta el PDF
        dot.render('tree', view=True)

    def add_node(self, dot, node):
        # Añade nodo al grafo
        dot.node(str(node.id), node.valor)

        # Añadir hijos al grafo
        if node.izq is not None:
            self.add_node(dot, node.izq)
            dot.edge(str(node.id), str(node.izq.id))

        if node.der is not None:
            self.add_node(dot, node.der)
            dot.edge(str(node.id), str(node.der.id))


'''
    Clase Nodo almacena el valor de un nodo del árbol de expresiones regulares.
'''
class Nodo:
    def __init__(self, valor, izq=None, der=None):
        self.id = uuid.uuid4()  # Genera ID unico del Nodo.
        self.valor = valor
        self.izq = izq
        self.der = der

        ascii = ord(valor)
        self.simbolo = Simbolo(ascii, valor)

        self.root = False
        self.analized = False

    def find_parent(self, root, node):
        # Si el nodo es la raiz, regresa None.
        if root == node:
            root.root = True
            return root

        # Revisa si el nodo esta en el hijo izquierdo de la raiz.
        if root.izq is not None:
            if root.izq == node:
                return root
            else:
                parent = self.find_parent(root.izq, node)
                if parent is not None:
                    return parent

        # Revisa si el nodo esta en el hijo derecho de la raiz.
        if root.der is not None:
            if root.der == node:
                return root
            else:
                parent = self.find_parent(root.der, node)
                if parent is not None:
                    return parent

        # Si no se encuentra el nodo, regresa None.
        return None

    def find_leftmost_leaf(self, root):
        # Si la raiz no tiene hijos, retorna la raiz.
        if root.izq is None and root.der is None:
            return root

        # Si la raiz tiene un hijo izquierdo, recursivamente recorre su subarbol izquierdo.
        if root.izq is not None:
            return self.find_leftmost_leaf(root.izq)
