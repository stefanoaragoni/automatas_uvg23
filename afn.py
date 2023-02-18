from automata import Automata

class AFN(Automata):
    def __init__(self, tree):
        self.tree = tree
        self.automata = Automata()

        self.init_automata()

    def init_automata(self):
        estados = []

    def subset_construction(self):
        pass
