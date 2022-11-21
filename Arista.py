class Arista:
    def __init__(self, origen, destino, peso) -> None:
        self.origen = origen
        self.destino = destino
        self.peso = peso

    def getOrigen(self):
        return self.origen

    def getDestino(self):
        return self.destino

    def getPeso(self):
        return self.peso
    
    def mostrar(self):
        print(f"{self.getOrigen()} - {self.getDestino()} - {self.getPeso()}")
