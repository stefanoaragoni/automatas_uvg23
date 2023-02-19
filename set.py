class Set:
    def __init__(self):
        self.Elementos = []
    
    def Interseccion(self, A):
        interseccion = Set()
        for item in self.Elementos:
            if item in A.Elementos:
                interseccion.AddItem(item)
        return interseccion
    
    def Union(self, A):
        union = Set()
        for item in self.Elementos:
            union.AddItem(item)
        for item in A.Elementos:
            union.AddItem(item)
        return union
    
    def Diferencia(self, A):
        diferencia = Set()
        for item in self.Elementos:
            if item not in A.Elementos:
                diferencia.AddItem(item)
        return diferencia
    
    def AddItem(self, item):
        if item not in self.Elementos:
            self.Elementos.append(item)

    def IsEmpty(self):
        return len(self.Elementos) == 0

    def returnLastItem(self):
        return self.Elementos[-1]

    def deleteItem(self, item):
        self.Elementos.remove(item)
