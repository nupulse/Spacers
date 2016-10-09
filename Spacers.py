#Spacers by nupulse 2016. Version 1.0
#Original core code from Mini Invaders by Nacho Cabanes

import pygame
from pygame.locals import *
import random

pygame.init()
pygame.display.set_icon(pygame.image.load('trooper.png'))
pygame.display.set_caption('Spacers')

ancho = 800
alto = 600
cantidadMarcianos = 10

pantalla = pygame.display.set_mode( (ancho, alto) )
pygame.key.set_repeat(1,25)
reloj = pygame.time.Clock()

fondo = pygame.image.load("fondo1.jpg")

#sonido
pygame.mixer.music.load("starwars.ogg")
pygame.mixer.music.play(1)

sonidolaser = pygame.mixer.Sound("disparo.ogg")
sonidoexplosion = pygame.mixer.Sound("explosion.ogg")
interludio = pygame.mixer.Sound("swinterludio.ogg")

imagenNave = pygame.image.load("falcon.png")
rectanguloNave = imagenNave.get_rect()
imagenUfo = pygame.image.load("deathstar.png")
rectanguloUfo = imagenUfo.get_rect()
imagenMarciano = pygame.image.load("tie.png")
rectangulosMarcianos = { }
marcianosVisibles = { }
velocidadesX = { }
velocidadesY = { }
imagenDisparo = pygame.image.load("laser.png")
rectanguloDisparo = imagenDisparo.get_rect()

imagenPresent = pygame.image.load("swportada.png")
rectanguloPresent = imagenPresent.get_rect()
rectanguloPresent.top = -20
rectanguloPresent.left = -10

letra30 = pygame.font.SysFont("Arial", 30)
imagenTextoPresent = letra30.render(' Pulsa Espacio para jugar', True, (200, 200, 200), (0, 0, 0) )
rectanguloTextoPresent = imagenTextoPresent.get_rect()
rectanguloTextoPresent.centerx = pantalla.get_rect().centerx
rectanguloTextoPresent.centery = 250

letra18 = pygame.font.SysFont("Arial", 18)

partidaEnMarcha = True

while partidaEnMarcha:

    # ---- Presentacion ----
    pantalla.fill((0, 0, 0))
    pantalla.blit(imagenPresent, rectanguloPresent)
    pantalla.blit(imagenTextoPresent, rectanguloTextoPresent)# Nuevo 0.09
    pygame.display.flip()

    entrarAlJuego = False
    while not entrarAlJuego:
        pygame.time.wait(100)
        for event in pygame.event.get(KEYUP):
            if event.key == K_SPACE:
                entrarAlJuego = True
                interludio.stop()

    # ---- Comienzo de una sesion de juego ----
    puntos = 0
    pygame.mixer.music.stop()
    rectanguloNave.left = ancho / 2
    rectanguloNave.top = alto - 80
    rectanguloUfo.top = 20

    for i in range(0, cantidadMarcianos + 1):
        rectangulosMarcianos[i] = imagenMarciano.get_rect()
        rectangulosMarcianos[i].left = random.randrange(50, 751)
        rectangulosMarcianos[i].top = random.randrange(10, 301)
        marcianosVisibles[i] = True
        velocidadesX[i] = 3
        velocidadesY[i] = 3

    disparoActivo = False
    ufoVisible = True
    terminado = False

    while not terminado:
        # ---- Comprobar acciones del usuario ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminado = True
                partidaEnMarcha = False

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            rectanguloNave.left -= 8
        if keys[K_RIGHT]:
            rectanguloNave.left += 8
        if rectanguloNave.left < 0:
            rectanguloNave.left = 0
        if rectanguloNave.right > ancho:
            rectanguloNave.right = 800

        if keys[K_SPACE] and not disparoActivo:
            disparoActivo = True
            rectanguloDisparo.left = rectanguloNave.left + 18
            rectanguloDisparo.top = rectanguloNave.top - 25
            sonidolaser.play()

         # ---- Actualizar estado ----
        for i in range(0, cantidadMarcianos + 1):
            rectangulosMarcianos[i].left += velocidadesX[i]
            rectangulosMarcianos[i].top += velocidadesY[i]
            if rectangulosMarcianos[i].left < 0 or rectangulosMarcianos[i].right > ancho:
                velocidadesX[i] = -velocidadesX[i]
            if rectangulosMarcianos[i].top < 0 or rectangulosMarcianos[i].bottom > alto:
                velocidadesY[i] = -velocidadesY[i]

        rectanguloUfo.left += 2
        if rectanguloUfo.right > ancho:
            rectanguloUfo.left = 0

        if disparoActivo:
            rectanguloDisparo.top -= 6
            if rectanguloDisparo.top <= 0:
                disparoActivo = False

        # ---- Comprobar colisiones ----
        for i in range(0, cantidadMarcianos + 1):
            if marcianosVisibles[i]:
                if rectanguloNave.colliderect(rectangulosMarcianos[i]):
                    terminado = True
                    interludio.play()

                if disparoActivo:
                    if rectanguloDisparo.colliderect(rectangulosMarcianos[i]):
                        marcianosVisibles[i] = False
                        disparoActivo = False
                        sonidoexplosion.play()
                        puntos += 10

        if disparoActivo:
            if rectanguloDisparo.colliderect(rectanguloUfo):
                ufoVisible = False
                disparoActivo = False
                sonidoexplosion.play()
                puntos += 50

        cantidadMarcianosVisibles = 0
        for i in range(0, cantidadMarcianos + 1):
            if marcianosVisibles[i]:
                cantidadMarcianosVisibles = cantidadMarcianosVisibles + 1

        #subir nivel
        if not ufoVisible and cantidadMarcianosVisibles == 0:
            for i in range(0, cantidadMarcianos + 1):
                rectangulosMarcianos[i] = imagenMarciano.get_rect()
                rectangulosMarcianos[i].left = random.randrange(50, 751)
                rectangulosMarcianos[i].top = random.randrange(10, 301)
                marcianosVisibles[i] = True

                velocidadesX[i] = 5
                velocidadesY[i] = 5

                ufoVisible = True


                # ---- Dibujar elementos en pantalla ----
        pantalla.fill((0, 0, 0))
        pantalla.blit(fondo, (0, 0))
        for i in range(0, cantidadMarcianos + 1):
            if marcianosVisibles[i]:
                pantalla.blit(imagenMarciano, rectangulosMarcianos[i])
        if ufoVisible:
            pantalla.blit(imagenUfo, rectanguloUfo)
        if disparoActivo:
            pantalla.blit(imagenDisparo, rectanguloDisparo)
        pantalla.blit(imagenNave, rectanguloNave)

        imagenPuntos = letra18.render('Puntos ' +str(puntos), True, (200,200,200), (0,0,0))
        rectanguloPuntos = imagenPuntos.get_rect()
        rectanguloPuntos.left = 10
        rectanguloPuntos.top = 10
        pantalla.blit(imagenPuntos, rectanguloPuntos)

        pygame.display.flip()

        # ---- Ralentizar hasta 40 fotogramas por segundo  ----
        reloj.tick(60)

# ---- Final de partida ----
pygame.quit()

# http://www.nachocabanes.com/python/pygame09.php
