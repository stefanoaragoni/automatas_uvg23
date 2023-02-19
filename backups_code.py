def afn_concatenacion(self, hojaIzq, hojaDer):
    a = None

    # Si el nodo izquierdo es un simbolo y no hay estados almacenados, crear un estado inicial
    if (self.Estados.IsEmpty() or (hojaIzq.valor != '*' and hojaIzq.valor != '|' and hojaIzq.valor != '.' and hojaIzq.analized == False)):
        a = Estado(self.count_estados)
        self.count_estados += 1
        self.Estados.AddItem(a)
        self.estado_inicial = a
    
    # Encontrar utlimo estado almacenado
    else:
        a = self.Estados.returnLastItem()
    

    b = self.count_estados
    if(hojaDer.izq == None):
        b = Estado(self.count_estados)
        self.count_estados += 1
        self.Estados.AddItem(b)

    else:
        self.afn_construction(hojaDer.izq)

        # Encontrar estado con id = b
        for estado in self.Estados.Elementos:
            if estado.id == b:
                b = estado
                break

    # Agregar transicion
    if hojaIzq.analized == False:
        c = Estado(self.count_estados)
        self.count_estados += 1
        self.Estados.AddItem(c)

        self.transiciones.append(Transicion(a, b, hojaIzq.simbolo))
        self.transiciones.append(Transicion(b, c, hojaDer.simbolo))
    else:
        self.transiciones.append(Transicion(a, b, hojaDer.simbolo))

    padre = self.tree.find_parent(self.tree, hojaIzq)
    padre.analized = True

    padre2 = self.tree.find_parent(self.tree, padre)
    self.afn_construction(padre2)