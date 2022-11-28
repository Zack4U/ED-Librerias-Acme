import json
import pygame
from pygame import *
from tkinter import ttk
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

    def crearInterfaz(self, screen):
        self.crearVentanas((0, 520, 1280, 200), screen)
        self.crearVentanas((1080, 0, 200, 520), screen)

        self.obstruirBtn(screen)
        self.moverProdundidadBtn(screen)
        self.moverAnchuraBtn(screen)

    def crearVentanas(self, rect, screen):
        self.ventana = draw.rect(screen, self.color_bg, rect)

    def dibujarBotones(self, rect, color, screen):
        pygame.draw.rect(screen, color, rect)

    def obstruirBtn(self, screen):
        self.obstruir = Rect((10, 530, 50, 50))
        color = (55, 55, 55)
        self.dibujarBotones(self.obstruir, color, screen)

    def moverProdundidadBtn(self, screen):
        self.moverProfundidad = Rect((70, 530, 50, 50))
        color = (55, 55, 55)
        self.dibujarBotones(self.moverProfundidad, color, screen)

    def moverAnchuraBtn(self, screen):
        self.moverAnchura = Rect((130, 530, 50, 50))
        color = (55, 55, 55)
        self.dibujarBotones(self.moverAnchura, color, screen)

    def obstruirPanel(self):
        self.close = False
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
        self.close = True

    def obstruirFn(self, origen, destino):
        self.grafo.bloquearArista(origen.get(), destino.get())

    def pulsarBotones(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == True:
            if self.moverProfundidad.collidepoint(mouse.get_pos()) and self.close:
                self.libs.recorridoProfundidad()
            if self.moverAnchura.collidepoint(mouse.get_pos()) and self.close:
                self.libs.recorridoAnchura()
            if self.obstruir.collidepoint(mouse.get_pos()) and self.close:
                self.obstruirPanel()
