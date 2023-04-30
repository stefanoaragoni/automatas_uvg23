from graphviz import Digraph
from automata import Automata

def Graph(automata, regex, type):
    dot = Digraph()

    # Atributos del grafo
    #dot.attr(rankdir="LR")
    #tempStr = str("\ "+type+" ["+regex+"] ")
    #dot.attr(label=tempStr)
    dot.attr(fontsize='20')
    
    # Agrega estado inicial
    dot.attr('node', shape='circle')
    dot.node("", shape='none',height='0',width='0')
    dot.node(str(automata.estado_inicial.id), shape="circle", color="blue")
    dot.edge("", str(automata.estado_inicial.id))

    # Agrega estados finales
    for final_state in automata.EstadosFinales.Elementos:
        dot.node(str(final_state.id), shape="circle", peripheries="2", color="red")

    # Agrega estados y transiciones
    for estado in automata.Estados.Elementos:
        if estado != automata.estado_inicial and estado not in automata.EstadosFinales.Elementos:
            dot.node(str(estado.id), shape="circle")

    for transicion in automata.transiciones:
        simbolo = transicion.el_simbolo.c_id.replace("'", "").replace('"', '')
        # check if symbol is numeric
        if simbolo.isnumeric():
            simbolo = chr(int(simbolo))

        dot.edge(str(transicion.estado_origen.id), str(transicion.estado_destino.id), label=simbolo)

    # Render graph
    dot.render(type, view=True, format='pdf')
