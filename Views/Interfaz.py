import json
import pygame
from pygame import *
from tkinter import PhotoImage, ttk
from tkinter import messagebox as MB
import tkinter as tk

from Models.Grafo import Grafo


class Interfaz():

    def __init__(self, libs):
        self.color_bg = (0, 0, 0)
        self.color_btn = (51, 51, 51)
        self.close = True

        self.libs = libs
        self.grafo = libs.grafo
        self.fuente = pygame.font.SysFont("comicsansms", 20)

    def crearInterfaz(self, screen):
        self.crearVentanas((0, 520, 1280, 200), screen)
        self.crearVentanas((1080, 0, 200, 520), screen)

        self.obstruirBtn(screen)
        self.moverProdundidadBtn(screen)
        self.moverAnchuraBtn(screen)
        self.moverLibreriaBtn(screen)
        self.caminoCortoBtn(screen)
        self.caminoCortoOrigenBtn(screen)
        self.refrescarBtn(screen)
        self.ordenCaminosBtn(screen)
        self.desObstruirBtn(screen)
        self.LETREROACME(screen)

    def crearVentanas(self, rect, screen):
        self.ventana = draw.rect(screen, self.color_bg, rect)

    def dibujarBotones(self, rect, color, text, screen):
        pygame.draw.rect(screen, color, rect)
        text = self.fuente.render(text, 1, (255, 255, 255))
        screen.blit(text, (rect.x+(rect.width-text.get_width())/2,
                           rect.y+(rect.height-text.get_height())/2))

    # * FUNCIONES DE LOS BOTONES

    def desObstruirPanel(self):
        main = tk.Tk()
        main.title("Liberar")

        tk.Label(main, text="PANEL DE LIBERACIONES",
                 font=('None', 20)).pack(pady=50, padx=20)
        tk.Label(main, text="Origen:",
                 font=('None', 15)).pack(pady=20)
        origen = ttk.Combobox(main, state="readonly",
                              values=self.grafo.getListaVertices())
        origen.pack(pady=10)
        tk.Label(main, text="Destino:",
                 font=('None', 15)).pack(pady=20)
        destino = ttk.Combobox(main, state="readonly",
                               values=self.grafo.getListaVertices())
        destino.pack(pady=10)
        tk.Button(text="LIBERAR", font=(
            "None", 20), bg="red", command=lambda: self.desObstruirFn(origen, destino)).pack(pady=50)
        main.mainloop()

    def obstruirPanel(self):
        main = tk.Tk()
        main.title("Obstruir")

        tk.Label(main, text="PANEL DE OBSTRUCCIONES",
                 font=('None', 20)).pack(pady=50, padx=20)
        tk.Label(main, text="Origen:",
                 font=('None', 15)).pack(pady=20)
        origen = ttk.Combobox(main, state="readonly",
                              values=self.grafo.getListaVertices())
        origen.pack(pady=10)
        tk.Label(main, text="Destino:",
                 font=('None', 15)).pack(pady=20)
        destino = ttk.Combobox(main, state="readonly",
                               values=self.grafo.getListaVertices())
        destino.pack(pady=10)
        tk.Button(text="OBSTRUIR", font=(
            "None", 20), bg="red", command=lambda: self.obstruirFn(origen, destino)).pack(pady=50)
        main.mainloop()

    def moverLibreriaFn(self):
        main = tk.Tk()
        main.title("Mover")

        tk.Label(main, text="PANEL DE DESTINOS",
                 font=('None', 20)).pack(pady=50, padx=20)
        tk.Label(main, text="Destino:",
                 font=('None', 15)).pack(pady=20)
        destino = ttk.Combobox(main, state="readonly",
                               values=self.grafo.getListaVertices())
        destino.pack(pady=10)
        tk.Button(text="INICIAR", font=(
            "None", 20), bg="red", command=lambda: self.libs.moverLibreria(destino.get())).pack(pady=50)

        main.mainloop()

    def obstruirFn(self, origen, destino):
        self.grafo.bloquearArista(origen.get(), destino.get())

    def desObstruirFn(self, origen, destino):
        self.grafo.liberarArista(origen.get(), destino.get())

    def caminoCortoFn(self):
        main = tk.Tk()
        main.title("Camino mas Corto")

        tk.Label(main, text="PANEL DE ORIGENES",
                 font=('None', 20)).pack(pady=50, padx=20)
        tk.Label(main, text="ORIGENES:",
                 font=('None', 15)).pack(pady=20)
        destino = ttk.Combobox(main, state="readonly",
                               values=self.grafo.getListaVertices())
        destino.pack(pady=10)
        tk.Button(text="MOSTRAR", font=(
            "None", 20), bg="red", command=lambda: self.libs.caminoCortoOrigen(destino.get())).pack(pady=50)
        main.mainloop()

    def ordenCaminos(self):
        main = tk.Tk()
        main.title("Sucursales en ORden")
        lista = tk.StringVar()
        tk.Label(main, text="Ingrese Datos",
                 font=('None', 20)).pack(pady=50, padx=20)
        tk.Label(main, text="ORIGENES:",
                 font=('None', 15)).pack(pady=20)
        entry = ttk.Combobox(main, state="readonly",
                             values=self.grafo.getListaVertices())
        verEntry = tk.Entry(
            main, width=50, state="readonly", textvariable=lista, font=("None", 10), )
        entry.pack(pady=20)
        tk.Button(text="INGRESAR", font=(
            "None", 18), bg="green", command=lambda: self.agregarTexto(lista, entry.get(), verEntry)).pack(pady=20)
        verEntry.pack(pady=20, padx=20)
        tk.Button(text="MOSTRAR", font=(
            "None", 20), bg="red", command=lambda: self.libs.libreriasOrden(verEntry.get())).pack(pady=50)
        main.mainloop()

    def agregarTexto(self, lista, texto, entry):
        lista.set(f"{lista.get()} {texto}")

    # * BOTONES
    def obstruirBtn(self, screen):
        self.obstruir = Rect((10, 530, 140, 50))
        color = (55, 55, 55)
        self.dibujarBotones(self.obstruir, color, "OBSTRUIR", screen)

    def desObstruirBtn(self, screen):
        self.desObstruir = Rect((10, 600, 140, 50))
        color = (55, 55, 55)
        self.dibujarBotones(self.desObstruir, color, "LIBERAR", screen)

    def moverProdundidadBtn(self, screen):
        self.moverProfundidad = Rect((170, 530, 180, 50))
        color = (55, 55, 55)
        self.dibujarBotones(self.moverProfundidad, color,
                            "R. PROFUNDIDAD", screen)

    def moverAnchuraBtn(self, screen):
        self.moverAnchura = Rect((170, 600, 180, 50))
        color = (55, 55, 55)
        self.dibujarBotones(self.moverAnchura, color, "R. ANCHURA", screen)

    def moverLibreriaBtn(self, screen):
        self.moverLibreria = Rect((370, 530, 120, 120))
        color = (55, 55, 55)
        self.dibujarBotones(self.moverLibreria, color, "ENVIAR A", screen)

    def caminoCortoBtn(self, screen):
        self.caminoCorto = Rect((510, 530, 200, 50))
        color = (55, 55, 55)
        self.dibujarBotones(self.caminoCorto, color, "CAMINOS CORTOS", screen)

    def caminoCortoOrigenBtn(self, screen):
        self.caminoCortoO = Rect((730, 530, 200, 50))
        color = (55, 55, 55)
        self.dibujarBotones(self.caminoCortoO, color,
                            "C. CORTO ORIGEN", screen)

    def refrescarBtn(self, screen):
        self.refrescar = Rect((510, 600, 420, 50))
        color = (55, 55, 55)
        self.dibujarBotones(self.refrescar, color, "REFRESCAR", screen)

    def ordenCaminosBtn(self, screen):
        self.orden = Rect((950, 530, 120, 120))
        color = (55, 55, 55)
        self.dibujarBotones(self.orden, color, "R. ORDEN", screen)

    def LETREROACME(self, screen):
        self.letrero = Rect((10, 660, 1060, 50))
        color = (255, 0, 0)
        self.dibujarBotones(self.letrero, color,
                            "LIBERIAS ACME - MAPA DE LIBRERIAS", screen)

    # * Listeners de los botones
    def pulsarBotones(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == True:
            if self.moverProfundidad.collidepoint(mouse.get_pos()) and self.close:
                self.libs.recorridoProfundidad()
            if self.moverAnchura.collidepoint(mouse.get_pos()) and self.close:
                self.libs.recorridoAnchura()
            if self.moverLibreria.collidepoint(mouse.get_pos()) and self.close:
                self.moverLibreriaFn()
            if self.caminoCorto.collidepoint(mouse.get_pos()) and self.close:
                self.libs.caminoCorto("Casita")
            if self.caminoCortoO.collidepoint(mouse.get_pos()) and self.close:
                self.caminoCortoFn()
            if self.orden.collidepoint(mouse.get_pos()) and self.close:
                self.ordenCaminos()
            if self.refrescar.collidepoint(mouse.get_pos()) and self.close:
                self.libs.refrescar()
            if self.obstruir.collidepoint(mouse.get_pos()) and self.close:
                self.obstruirPanel()
            if self.desObstruir.collidepoint(mouse.get_pos()) and self.close:
                self.desObstruirPanel()
