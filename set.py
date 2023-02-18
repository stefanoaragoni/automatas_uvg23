from abc import ABC, abstractmethod

class Set:
    def __init__(self):
        self.Elementos = []
    
    @abstractmethod
    def Interseccion(self, A):
        pass
    
    @abstractmethod
    def Union(self, A):
        pass
    
    @abstractmethod
    def Diferencia(self, A):
        pass
    
    def AddItem(self, item):
        if item not in self.Elementos:
            self.Elementos.append(item)
