class Arista:
    def __init__(self, origen, destino, peso, color=(255, 255, 255)) -> None:
        self.origen = origen
        self.destino = destino
        self.peso = peso
        self.color = color

    def getOrigen(self):
        return self.origen

    def getDestino(self):
        return self.destino

    def getPeso(self):
        return self.peso

    def mostrar(self):
        print(f"{self.getOrigen()} - {self.getDestino()} - {self.getPeso()}")
