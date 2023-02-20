from estado import Estado
from simbolo import Simbolo

class Transicion:
    def __init__(self, estado_origen, estado_destino, el_simbolo):
        self.estado_origen = estado_origen
        self.estado_destino = estado_destino
        self.el_simbolo = el_simbolo
