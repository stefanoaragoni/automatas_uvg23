from graphviz import Digraph
from automata import Automata
from afn import AFN

def Graph(automata, regex, type):
    dot = Digraph()

    # Set graph attributes
    dot.attr(rankdir="LR")
    tempStr = str("\ "+type+" ["+regex+"] ")
    dot.attr(label=tempStr)
    dot.attr(fontsize='20')
    
    # Add initial state
    dot.attr('node', shape='circle')
    dot.node("", shape='none',height='0',width='0')
    dot.node(str(automata.estado_inicial.id), shape="circle")
    dot.edge("", str(automata.estado_inicial.id))

    # Add final states
    for final_state in automata.EstadosFinales.Elementos:
        dot.node(str(final_state.id), shape="circle", peripheries="2")

    # Add states and transitions
    for estado in automata.Estados.Elementos:
        if estado != automata.estado_inicial and estado not in automata.EstadosFinales.Elementos:
            dot.node(str(estado.id), shape="circle")

    for transicion in automata.transiciones:
        dot.edge(str(transicion.estado_origen.id), str(transicion.estado_destino.id), label=transicion.el_simbolo.c_id)

    # Render graph
    dot.render("automata", view=True)
