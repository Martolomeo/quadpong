#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos

import sys, pygame, random
from pygame.locals import *
 
# Constantes

WIDTH = 640
HEIGHT = 480
 
# Clases
# ---------------------------------------------------------------------

class Bola(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("bola.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed = [0.1, 0.1]
        self.vel_x = random.randint(1,4)
        self.vel_y = 5 - self.vel_x
        self.mod = 1
        if random.randint(1,2) == 1:
            self.vely = -1
        else:
            self.vely = 1
        if random.randint(1,2) == 1:
            self.velx = 1
        else:
            self.velx = -1

    def actualizar(self, n, pala_0, pala_1, pala_2, pala_3, puntos):
        self.rect.centerx += self.speed[0] * n * self.vel_x * self.velx * self.mod
        self.rect.centery += self.speed[1] * n * self.vel_y * self.vely * self.mod

        if self.rect.left <= 0 or self.rect.top <=0:
            puntos[1] += 1
            self.rect.centerx = WIDTH/2
            self.rect.centery = HEIGHT/2
            self.vel_x = random.randint(1,4)
            self.vel_y = 5 - self.vel_x
            if random.randint(1,2) == 1:
                self.vely = -1
            else:
                self.vely = 1
            if random.randint(1,2) == 1:
                self.velx = 1
            else:
                self.velx = -1
            self.mod = 1
            
        if self.rect.right >= WIDTH or self.rect.bottom >= HEIGHT:
            puntos[0] += 1
            self.rect.centerx = WIDTH/2
            self.rect.centery = HEIGHT/2
            self.vel_x = random.randint(1,4)
            self.vel_y = 5 - self.vel_x
            if random.randint(1,2) == 1:
                self.vely = -1
            else:
                self.vely = 1
            if random.randint(1,2) == 1:
                self.velx = 1
            else:
                self.velx = -1          
            self.mod = 1
 
        if pygame.sprite.collide_rect(self, pala_0) or pygame.sprite.collide_rect(self, pala_1):
            self.speed[0] = -self.speed[0]
            self.mod += 0.1
            self.rect.centerx += self.speed[0] * n

        if pygame.sprite.collide_rect(self, pala_2) or pygame.sprite.collide_rect(self, pala_3):
            self.speed[1] = -self.speed[1]
            self.mod += 0.1
            self.rect.centery += self.speed[1] * n

        return puntos

class Pala_v(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("pala_v.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = HEIGHT / 2
        self.speed = 0.8

    def moverv(self, n, keys):
        if self.rect.top >= 0:
            if keys[K_UP]:
                self.rect.top -= self.speed * n
        if self.rect.bottom <= HEIGHT:
            if keys[K_DOWN]:
                self.rect.bottom += self.speed * n
                
    def moverv1(self, n, keys):
        if self.rect.top >= 0:
            if keys[K_w]:
                self.rect.top -= self.speed * n
        if self.rect.bottom <= HEIGHT:
            if keys[K_s]:
                self.rect.bottom += self.speed * n

    def ia(self, n, bola):
        if bola.rect.centery < self.rect.centery:
            self.rect.centery -= self.speed * n
        if bola.rect.centery > self.rect.centery:
            self.rect.centery += self.speed * n

class Pala_h(pygame.sprite.Sprite):
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("pala_h.png")
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = WIDTH/2
        self.speed = 0.8

    def moverh(self,n,keys):
        if self.rect.left >= 0:
            if keys[K_LEFT]:
                self.rect.centerx -= self.speed * n
        if self.rect.right <= WIDTH:
            if keys[K_RIGHT]:
                self.rect.centerx += self.speed * n

    def moverh1(self,n,keys):
        if self.rect.left >= 0:
            if keys[K_a]:
                self.rect.centerx -= self.speed * n
        if self.rect.right <= WIDTH:
            if keys[K_d]:
                self.rect.centerx += self.speed * n

    def ia(self,n,bola):
        if bola.rect.centerx > self.rect.centerx:
            self.rect.centerx += self.speed * n
        if bola.rect.centerx < self.rect.centerx:
            self.rect.centerx -= self.speed * n

 
# ---------------------------------------------------------------------
 
# Funciones
# ---------------------------------------------------------------------

def load_image(filename, transparent=False):
        try: image = pygame.image.load(filename)
        except pygame.error, message:
                raise SystemExit, message
        image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)
        return image

def texto(texto, posx, posy, tamano, color=(255, 255, 255)):
    fuente = pygame.font.Font("DroidSans.ttf", tamano)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect

# ---------------------------------------------------------------------
 
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pruebas Pygame")

    background_image = load_image('fondo.png')
    bola = Bola()
    pala_0 = Pala_v(10)
    pala_1 = Pala_v(WIDTH - 10)
    pala_2 = Pala_h(10)
    pala_3 = Pala_h(HEIGHT - 10)
    clock = pygame.time.Clock()
    puntos = [0,0]

    while True:
        keys = pygame.key.get_pressed()
        tiempo = clock.tick(60)
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit()
                pygame.quit()
        
        punto = bola.actualizar(tiempo, pala_0, pala_1, pala_2, pala_3, puntos)
        pala_0.moverv(tiempo, keys)
        pala_1.moverv1(tiempo, keys)
        pala_2.moverh(tiempo, keys)
        pala_3.moverh1(tiempo, keys)

        p_1, p_1_rect = texto(str(puntos[0]), 160, 240, 25)
        p_2, p_2_rect = texto(str(puntos[1]), 480, 240, 25)
        p1, p1_rect = texto("Puntaje J1", 145, 200, 15, (0,0,0))
        p2, p2_rect = texto("Puntaje J2", 465, 200, 15, (0,0,0))

        screen.blit(background_image, (0,0))
        screen.blit(p_1, p_1_rect)
        screen.blit(p_2, p_2_rect)
        screen.blit(p1, p1_rect)
        screen.blit(p2, p2_rect)
        screen.blit(bola.image, bola.rect)
        screen.blit(pala_0.image, pala_0.rect)
        screen.blit(pala_1.image, pala_1.rect)
        screen.blit(pala_2.image, pala_2.rect)
        screen.blit(pala_3.image, pala_3.rect)
        pygame.display.flip()
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()
