from Models.Arista import Arista
from Models.Vertice import Vertice


class Librerias():

    def __init__(self):

        # Iniciarlizar librerias
        LibreriaGadner = Vertice()
        LibreriaEuler = Vertice()
        LibreriaKonisberg = Vertice()
        LibreriaVoronoi = Vertice()
        LibreriaGauss = Vertice()
        LibreriaRichter = Vertice()
        LibreriaFibonacci = Vertice()
        LibreriaFahrenheit = Vertice()
        LibreriaHilbert = Vertice()
        LibreriaCelsius = Vertice()

    def init_aristas(self):

        aGadnerEuler = Arista()
        aGadnerFibonacci = Arista()
        aGadnerEuler = Arista()
        aGadnerVoronoi = Arista()

        aEulerGadner = Arista()
        aEulerVoronoi = Arista()
        aEulerCasita = Arista()
