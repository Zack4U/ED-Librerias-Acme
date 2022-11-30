import json
from threading import Thread
from time import sleep
import pygame
from Models.Arista import *
from Models.Grafo import *
from Models.Vertice import *


class Librerias():

    def __init__(self, velocidad, screen):

        self.grafo = Grafo()
        self.screen = screen

        self.libreria = pygame.image.load("Resources/libreria.png")
        self.libreria = pygame.transform.scale(self.libreria, (100, 70))
        self.casita = pygame.image.load("Resources/casa.png")
        self.casita = pygame.transform.scale(self.casita, (100, 70))
        self.mensajero = pygame.image.load("Resources/mensajero.png")
        self.mensajero = pygame.transform.scale(self.mensajero, (100, 70))

        self.velocidad = velocidad
        self.tolerancia = self.velocidad*5+1
        self.stop = False
        self.disponible = True

        self.leerJson()
        self.crearGrafo()
        self.crearMensajero()

    def leerJson(self):
        with open("Data/libs.json", "r") as libsJson:
            libs = json.load(libsJson)
        libsJson.close()
        self.vertices = libs['vertices']
        self.aristas = libs['aristas']
        self.ubicaciones = libs['ubicaciones']

    def crearGrafo(self):
        # * Creacion de los nodos
        for node in self.vertices:
            self.grafo.ingresarVertices(node)

        # * Creacion de las aristas
        for key, value in self.aristas.items():
            self.grafo.ingresarArista(
                value['from'], value['to'], value['data'])

    def mostrarLibrerias(self, screen):
        for lib in self.grafo.listaVertices:
            self.dibujarLibreria(lib, screen)

    def dibujarLibreria(self, lib, screen):
        if lib == self.grafo.obtenerOrigen("Casita"):
            rect = self.casita.get_rect()
            rect.center = self.ubicaciones[lib.dato][0], self.ubicaciones[lib.dato][1]
            screen.blit(self.casita, rect)
        else:
            rect = self.libreria.get_rect()
            rect.center = self.ubicaciones[lib.dato][0], self.ubicaciones[lib.dato][1]
            screen.blit(self.libreria, rect)
        self.dibujarTxtLib(lib, rect, screen)

    def dibujarTxtLib(self, lib, rect, screen):
        fuente = pygame.freetype.SysFont("comicsansms", 0)
        fuente.render_to(screen, rect, lib.dato, (255, 255, 255), bgcolor=(0, 0, 255),
                         size=20)

    def mostrarRutas(self, screen):
        for ruta in self.grafo.listaAristas:
            self.dibujarLineas(ruta, screen)

    def dibujarLineas(self, ruta, screen):
        color = self.grafo.obtenerArista(ruta.origen, ruta.destino)[0].color
        color2 = self.grafo.obtenerArista(ruta.origen, ruta.destino)[1].color
        if color != color2 or color2 != color:
            color = color2
        start = self.ubicaciones[ruta.getOrigen()]
        end = self.ubicaciones[ruta.getDestino()]
        pygame.draw.line(screen, color, (start[0], start[1]), (end[0], end[1]))

    def mostrarPesos(self, screen):
        for ruta in self.grafo.listaAristas:
            self.dibujarPesos(ruta, screen)

    def dibujarPesos(self, ruta, screen):
        start = self.ubicaciones[ruta.getOrigen()]
        end = self.ubicaciones[ruta.getDestino()]
        data = str(ruta.getPeso())
        fuente = pygame.freetype.SysFont("comicsansms", 0)
        text_rect = fuente.get_rect(data, size=20, )
        text_rect.center = int((start[0]+end[0])/2), int((start[1]+end[1])/2)

        fuente.render_to(screen, text_rect, data, (0, 0, 0), bgcolor=(255, 255, 255),
                         size=20)

    def crearMensajero(self):
        self.mensajero_rect = self.mensajero.get_rect()
        self.mensajero_rect.center = self.ubicaciones['Casita'][0], self.ubicaciones['Casita'][1]

    def monstrarMensajero(self, screen):
        screen.blit(self.mensajero, self.mensajero_rect)

    def mover(self, ubicacion):
        ubicacion = [ubicacion[0], ubicacion[1]]
        if (self.mensajero_rect.centerx >= ubicacion[0]-self.tolerancia and self.mensajero_rect.centerx <= ubicacion[0]+self.tolerancia
                and self.mensajero_rect.centery >= ubicacion[1]-self.tolerancia and self.mensajero_rect.centery <= ubicacion[1]+self.tolerancia):
            return True
        if self.mensajero_rect.centerx < ubicacion[0]:
            self.mensajero_rect.centerx += self.velocidad
        if self.mensajero_rect.centerx > ubicacion[0]:
            self.mensajero_rect.centerx -= self.velocidad
        if self.mensajero_rect.centery < ubicacion[1]:
            self.mensajero_rect.centery += self.velocidad
        if self.mensajero_rect.centery > ubicacion[1]:
            self.mensajero_rect.centery -= self.velocidad

    def mandarMensajero(self, ruta):
        if self.stop == False:
            self.thread = Thread(target=lambda: self.moverMensajero(ruta))
            self.thread.start()

    def moverMensajero(self, ruta):
        if self.disponible:
            self.disponible = False
            for v in ruta:
                if self.stop:
                    return
                while not (self.stop and v is None):
                    if v is None:
                        break
                    if self.stop:
                        return
                    u = self.ubicaciones[v]
                    if (self.mover(u)):
                        sleep(1)
                        break
                    sleep(0.01)
            self.volver(ruta)
            self.disponible = True

    def volver(self, ruta):
        ruta = ruta[::-1]
        ubicacion = ruta[0]
        ruta = self.grafo.dijsktra(ubicacion, "Casita")
        print(ruta)
        for v in ruta:
            if self.stop:
                return
            while not (self.stop and v is None):
                if v is None:
                    break
                if self.stop:
                    return
                u = self.ubicaciones[v]
                if (self.mover(u)):
                    sleep(1)
                    break
                sleep(0.01)

    def recorridoProfundidad(self):
        self.grafo.rProfundidad("Casita")
        r = self.grafo.visitadosCP
        ruta = []
        for i in range(len(r)-1):
            ini = r[i]
            end = r[i+1]
            for j in self.grafo.dijsktra(ini, end):
                ruta.append(j)
        self.mandarMensajero(ruta)

    def recorridoAnchura(self):
        self.grafo.rAnchura("Casita")
        r = self.grafo.visitadosCA
        ruta = []
        for i in range(len(r)-1):
            ini = r[i]
            end = r[i+1]
            for j in self.grafo.dijsktra(ini, end):
                ruta.append(j)
        self.mandarMensajero(ruta)

    def moverLibreria(self, libreria):
        print(libreria)
        ruta = self.grafo.dijsktra("Casita", libreria)
        print(ruta)
        self.mandarMensajero(ruta)

    def pintarAristas(self, color, ruta, screen):
        for r in ruta:
            self.dibujarLineas(r, screen, color)

    def caminoCorto(self, origen):
        ruta = self.grafo.Prim(origen)
        for i in ruta:
            for j in self.grafo.obtenerArista(i[0], i[1]):
                j.color = (0, 255, 0)

    def caminoCortoOrigen(self, origen):
        for v in self.grafo.listaVertices:
            if v.dato == origen:
                continue
            ruta = self.grafo.dijsktra(origen, v.dato)
            print(f"{origen} a {v.dato} es: {ruta}")
            for i in range(len(ruta)-1):
                for j in self.grafo.obtenerArista(ruta[i], ruta[i+1]):
                    j.color = (0, 255, 0)

    def refrescar(self):
        for i in self.grafo.listaAristas:
            i.color = (255, 255, 255)

    def libreriasOrden(self, ruta):
        r = ruta.split()
        ruta = []
        for i in range(len(r)-1):
            ini = r[i]
            end = r[i+1]
            for i in self.grafo.dijsktra(ini, end):
                ruta.append(i)
        self.mandarMensajero(ruta)
