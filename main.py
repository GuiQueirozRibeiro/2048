import numpy as np
import random
import pygame
from pygame.locals import *

from constantes import CP

N = 4

class Py2048:
    def __init__(self):
        self.matriz = np.zeros((N, N), dtype=int)

        self.W =400
        self.H = self.W
        self.SPACING = 10

        pygame.init()
        pygame.display.set_caption("2048")

        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
        self.screen = pygame.display.set_mode((self.W, self.H))

    def __str__(self):
        return str(self.matriz)

    def novoNumero(self, k=1):
        PosicaoLivre = list(zip(*np.where(self.matriz == 0)))
        for pos in random.sample(PosicaoLivre, k=k):
            if random.random() < .1:
                self.matriz[pos] = 4
            else:
                self.matriz[pos] = 2

    @staticmethod
    def pegarNumeros(this):
        this_n = this[this != 0]
        this_n_sum = []
        skip = False
        for j in range(len(this_n)):
            if skip:
                skip = False
                continue
            if j != len(this_n) - 1 and this_n[j] == this_n[j + 1]:
                new_n = this_n[j] * 2
                skip = True
            else:
                new_n = this_n[j]

            this_n_sum.append(new_n)
        return np.array(this_n_sum)

    def move(self, move):
        for i in range(N):
            if move in 'ed':
                this = self.matriz[i, :]
            else:
                this = self.matriz[:, i]

            flipped = False
            if move in 'db':
                flipped = True
                this = this[::-1]

            this_n = self.pegarNumeros(this)

            new_this = np.zeros_like(this)
            new_this[:len(this_n)] = this_n

            if flipped:
                new_this = new_this[::-1]

            if move in 'ed':
                self.matriz[i, :] = new_this
            else:
                self.matriz[:, i] = new_this

    def desenharJogo(self):
        self.screen.fill(CP['back'])

        for i in range(N):
            for j in range(N):
                n = self.matriz[i][j]

                rect_x = j * self.W // N + self.SPACING
                rect_y = i * self.H // N + self.SPACING
                rect_w = self.W // N - 2 * self.SPACING
                rect_h = self.H // N - 2 * self.SPACING

                pygame.draw.rect(self.screen,
                                 CP[n],
                                 pygame.Rect(rect_x, rect_y, rect_w, rect_h),
                                 border_radius=8)
                if n == 0:
                    continue
                text_surface = self.myfont.render(f'{n}', True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(rect_x + rect_w / 2,
                                                          rect_y + rect_h / 2))
                self.screen.blit(text_surface, text_rect)

    @staticmethod
    def esperarTecla():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 's'
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        return 'c'
                    elif event.key == K_RIGHT:
                        return 'd'
                    elif event.key == K_LEFT:
                        return 'e'
                    elif event.key == K_DOWN:
                        return 'b'
                    elif event.key == K_q or event.key == K_ESCAPE:
                        return 's'

    def gameOver(self):
        matriz_bu = self.matriz.copy()
        for move in 'edcb':
            self.move(move)
            if not all((self.matriz == matriz_bu).flatten()):
                self.matriz = matriz_bu
                return False
        return True

    def play(self):
        self.novoNumero(k=2)

        while True:
            self.desenharJogo()
            pygame.display.flip()
            cmd = self.esperarTecla()
            if cmd == 's':
                break

            antigaMatriz = self.matriz.copy()
            self.move(cmd)
            print(game.matriz)
            if self.gameOver():
                print('GAME OVER!')
                break

            if not all((self.matriz == antigaMatriz).flatten()):
                self.novoNumero()

game = Py2048()
game.play()
