class Vertice:
    def __init__(self, dato):
        self.dato = dato
        self.listaAdyacentes = []

    def getDato(self):
        return self.dato

    def getListaAdyacentes(self):
        return self.listaAdyacentes
