import numpy as np
import random
import pygame
from pygame.locals import *
import sys
from constants import CP

N = 4  # matrice patratica de 4 linii si 4 coloane


class Proiect2048:
    def __init__(self):
        self.grid = np.zeros((N, N), dtype=int)  # face matrice cu valori de 0 si date de tip int, adica numere intregi
        self.W = 400  # latime
        self.H = self.W  # inaltime
        self.SPACING = 10
        pygame.init()  # initializam jocul
        pygame.display.set_caption("2048")  # titlul jocului
        pygame.font.init()  # initializare font
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)  # formatul jocului si marimea caracterelor
        self.screen = pygame.display.set_mode((self.W, self.H))  # rezolutia jocului

    def new_number(self, k=1):  # Marian, k = 1 sa afiseze un numar random la fiecare mutare
        free_poss = list(zip(*np.where(self.grid == 0)))  # np.where returneaza pozitiile elementelor, zip grupeaza linie coloana
        for pos in random.sample(free_poss, k=k):  # random.sample(lista, k) iti returneaza k elemente random din lista ta
            if random.random() < .1:  # random.random() returneaza un numar intre 0 si 1
                self.grid[pos] = 4  # valoarea poate sa fie 4 (probabilitate de sub 10% [acel <.1])
            else:
                self.grid[pos] = 2  # dar poate sa fie si 2 (probabilitate mai mare - peste 90%)

    @staticmethod  # STATIC METHOD SA ZIC CE FACE
    def _get_nums(this):  # Sergiu
        this_n = this[this != 0]  # listele cu cifrele diferite de 0
        this_n_sum = []
        skip = False
        for j in range(len(this_n)):
            if skip:
                skip = False
                continue
            if j != len(this_n) - 1 and this_n[j] == this_n[j + 1]:  # daca ajungem la ultima pozitie, oprim
                new_n = this_n[j] * 2
                skip = True  # sarim peste cazul cand s-a facut operatia si ignoram al 2-lea numar
            else:
                new_n = this_n[j]

            this_n_sum.append(new_n)  # salveaza suma numerelor
        return np.array(this_n_sum)  # se face lista de tip numpy

    def make_move(self, move):  # Sergiu
        for i in range(N):
            if move in 'lr':  # daca este stanga sau dreapta
                this = self.grid[i, :]  # de la linia i la toate coloanele
            else:
                this = self.grid[:, i]  # ne folosim doar de coloane
            flipped = False
            if move in 'ud':  # daca este sus sau jos
                flipped = True
                this = this[::-1]  # o intoarcem si facem acelasi algoritm ca la stanga sau dreapta
            this_n = self._get_nums(this)
            new_this = np.zeros_like(this)  # reinitializam cu 0 pozitiile care s-au mutat
            new_this[:len(this_n)] = this_n  # numerele diferite de 0
            if flipped:
                new_this = new_this[::-1]
            if move in 'lr':
                self.grid[i, :] = new_this  # salvam liniile in matrice
            else:
                self.grid[:, i] = new_this  # salvam coloanele in matrice

    def draw_game(self):  # Marian
        self.screen.fill(CP['background'])  # culorile din background
        for i in range(N):
            for j in range(N):
                n = self.grid[i][j]
                rect_x = j * self.W // N + self.SPACING  # patratelele de pe linii si coloane
                rect_y = i * self.H // N + self.SPACING
                rect_w = self.W // N - 2 * self.SPACING  # spatierea patretelor pe latime si inaltime
                rect_h = self.H // N - 2 * self.SPACING
                pygame.draw.rect(self.screen,
                                 CP[n],
                                 pygame.Rect(rect_x, rect_y, rect_w, rect_h),
                                 border_radius=8)  # rotunjirea coltului
                if n == 0:  # ca sa nu printam 0 pe pozitii, nu vrem asta
                    continue  # si atunci sarim peste tot text_surface si _rect
                text_surface = self.myfont.render(f'{n}', True, (0, 0, 0))  # punem valorile/cifrele prin f string
                text_rect = text_surface.get_rect(center=(rect_x + rect_w / 2,  # punerea cifrelor in mijlocul patratelelor
                                                          rect_y + rect_h / 2))
                self.screen.blit(text_surface, text_rect)  # patratele cu valori

    @staticmethod
    def wait_for_key():  # Marian
        while True:
            for event in pygame.event.get():  # verifica toate evenimentele din pygame
                if event.type == QUIT:
                    return 'q'
                if event.type == KEYDOWN:  # cand o tasta este apasata
                    if event.key == K_UP:
                        return 'u'
                    elif event.key == K_RIGHT:
                        return 'r'
                    elif event.key == K_LEFT:
                        return 'l'
                    elif event.key == K_DOWN:
                        return 'd'
                    elif event.key == K_q or event.key == K_ESCAPE:  # o oprire fortata cu tasta q
                        return 'q'

    def game_over(self):  # David
        grid_bu = self.grid.copy()  # pt. ca make_move schimba grila, facem o copie
        # daca dupa prima miscare, se schimba, nu mai trebuie sa le verificam si pe restul
        for move in 'lrud':  # daca se face o miscare random, dar care sa nu inchida jocul
            self.make_move(move)
            if not all((self.grid == grid_bu).flatten()):  # flatten adica matricea o aranjeaza pe linie
                self.grid = grid_bu  # pentru ca se pot face miscari, atunci ne reintoarcem pe grila noastra precedenta
                return False  # jocul ii bun
        return True  # game over

    @staticmethod
    def end():  # David
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def game_over_text(self):  # David
        self.screen.fill(CP["menu"])  # culori background la joc
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:  # daca apas pe X (Close)
                    self.end()  # il inchide
            text = self.myfont.render("Ai pierdut!", True, CP["textfinish"])
            textpos = text.get_rect()
            textpos.center = (self.W // 2, self.H // 2)
            self.screen.blit(text, textpos)
            pygame.display.update()

    def play(self):
        self.new_number(k=2)  # initializam cele 2 pozitii cu valori (inceputul jocului)
        while True:
            self.draw_game()  # desenam patratelele pentru fiecare pozitie
            pygame.display.flip()
            cmd = self.wait_for_key()  # dam o comanda
            if cmd == 'q':
                break
            old_grid = self.grid.copy()
            self.make_move(cmd)
            print(game.grid)
            if self.game_over():
                self.game_over_text()
            if not all((self.grid == old_grid).flatten()):
                self.new_number()


if __name__ == '__main__':
    game = Proiect2048()
    game.play()