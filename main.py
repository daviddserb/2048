import numpy as np
import random
import pygame
import sys
from pygame.locals import *
from constants import CP

N = 4  # matrice patratica de 4 linii si 4 coloane
grid = np.zeros((N, N), dtype=int)  # variabilele de tip int
W = 400  # latime
H = W  # inaltime
SPACING = 10
pygame.init()  # initializam jocul
pygame.display.set_caption("2048")  # titlul jocului
pygame.font.init()  # initializare font
myfont = pygame.font.SysFont("Calibri", 30)  # formatul jocului si marimea caracterelor
screen = pygame.display.set_mode((W, H))  # rezolutia jocului


def new_number(k=1):  # Marian
    free_poss = list(zip(*np.where(grid == 0)))  # zip le grupeaza 2 cate 2, adica inainte lista era [(0,0,0,0,1,1,etc...)], acum este [(0,0),(0,1),(0,2),(0,3),(1,0),etc...]
    for pos in random.sample(free_poss, k=k):  # cand incepi jocul ai valori pe 2 pozitii (acel k)
        if random.random() < .1:  # pentru a fi 4 trebuie ca valoarea sa fie sub 10%
            grid[pos] = 4  # valoarea poate sa fie 4 (probabilitate de sub 10% [acel <.1])
        else:
            grid[pos] = 2  # dar poate sa fie si 2 (probabilitate mai mare - peste 90%)


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


def make_move(move):  # Sergiu
    for i in range(N):
        if move in "lr":  # daca este stanga sau dreapta
            this = grid[i, :]  # de la linia i la toate coloanele
        else:
            this = grid[:, i]  # ne folosim doar de coloane
        flipped = False
        if move in "ud":  # daca este sus sau jos
            flipped = True
            this = this[::-1]  # o intoarcem si facem acelasi algoritm ca la stanga sau dreapta
        this_n = _get_nums(this)
        new_this = np.zeros_like(this)  # reinitializam cu 0 pozitiile care s-au mutat
        new_this[:len(this_n)] = this_n  # numerele diferite de 0
        if flipped:
            new_this = new_this[::-1]
        if move in "lr":
            grid[i, :] = new_this  # salvam liniile in matrice
        else:
            grid[:, i] = new_this


def draw_game():  # Marian
    screen.fill(CP["background"])  # culorile din background

    for i in range(N):
        for j in range(N):
            n = grid[i][j]
            rect_x = j * W // N + SPACING  # patratelele de pe linii si coloane
            rect_y = i * H // N + SPACING
            rect_w = W // N - 2 * SPACING  # spatierea patretelor pe latime si inaltime
            rect_h = H // N - 2 * SPACING
            pygame.draw.rect(screen,
                             CP[n],
                             pygame.Rect(rect_x, rect_y, rect_w, rect_h),
                             border_radius=8)  # rotunjirea coltului
            if n == 0:  # ca sa nu printam 0 pe pozitii, nu vrem asta
                continue  # si atunci sarim peste tot text_surface si _rect
            text_surface = myfont.render(f"{n}", True, (0, 0, 0))  # punem valorile/cifrele prin f string
            text_rect = text_surface.get_rect(center=(rect_x + rect_w / 2,  # punerea cifrelor in mijlocul patratelelor
                                                      rect_y + rect_h / 2))
            screen.blit(text_surface, text_rect)  # patratele cu valori


def wait_for_key():  # Marian
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                end()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    return "u"
                elif event.key == K_RIGHT:
                    return "r"
                elif event.key == K_LEFT:
                    return "l"
                elif event.key == K_DOWN:
                    return "d"
                elif event.key == K_F1:  # o oprire fortata
                    menu()
                elif event.key == K_q or event.key == K_ESCAPE:
                    return "q"


def game_over():  # David
    global grid
    grid_bu = grid.copy()  # pt. ca make_move schimba grila, facem o copie
    # daca dupa prima miscare, se schimba, nu mai trebuie sa le verificam si pe restul
    for move in "lrud":  # daca se face o miscare random, dar care sa nu inchida jocul
        make_move(move)
        if not all((grid == grid_bu).flatten()):  # flatten adica matricea o aranjeaza pe linie
            grid = grid_bu  # pentru ca se pot face miscari, atunci ne reintoarcem pe grila noastra precedenta
            return False  # jocul ii bun
    return True  # game over


def end():  # David
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def play():  # David
    new_number(k=2)  # initializam cele 2 pozitii cu valori (inceputul jocului)
    while True:
        draw_game()  # desenam patratelele pentru fiecare pozitie
        pygame.display.flip()
        cmd = wait_for_key()  # dam o comanda
        old_grid = grid.copy()
        make_move(cmd)
        print(grid)
        if game_over():
            menu()
        if not all((grid == old_grid).flatten()):
            new_number()

