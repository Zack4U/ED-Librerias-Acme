from Views.Interfaz import Interfaz
from Views.Librerias import *
import pygame as pg
import sys


def main():
    game()


def events(event):
    if event.type == pg.QUIT:
        sys.exit()


def game():

    libs = Librerias()
    gui = Interfaz(libs.grafo)
    bg = pygame.image.load("Resources/mapa.jpg")
    bg = pygame.transform.scale(bg, (1280, 720))
    icon = pygame.image.load('Resources/icon.png')

    pg.init()

    size = width, height = 1280, 720
    screen = pg.display.set_mode(size)
    clock = pg.time.Clock()

    pygame.display.set_caption('Librerias ACME')
    pygame.display.set_icon(icon)

    activate = True

    while activate:
        for event in pg.event.get():
            events(event)
            gui.pulsarBotones(event)

        screen.blit(bg, (0, 0))

        libs.mostrarRutas(screen)
        libs.mostrarLibrerias(screen)
        libs.mostrarPesos(screen)
        libs.monstrarMensajero(screen)

        gui.crearInterfaz(screen)

        pg.display.flip()
        clock.tick(144)


if __name__ == '__main__':
    main()
