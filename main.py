import numpy as np  # este o biblioteca care adauga diferite functionalitati, in special pt. siruri si matrici
import random
import pygame  # un modul cu diferite biblioteci pentru scrierea jocurilor video
import sys  # un modul cu diferite variabile si functii pt. manipularea diferitelor parti a PRE
from pygame.locals import *
from constants import CP

import array as arr
array_1 = np.array([3, 4, 5, 6, 8]) / 2;
print(array_1)

N = 4
grid = np.zeros((N, N), dtype=int)  # declaram matricea patratica de 4, o initializam cu 0 si o declaram de tip int
W = 400  # latime
H = W  # inaltime
SPACING = 10

pygame.init()  # initializarea tuturor modulelor pygame importate
pygame.display.set_caption("2048")  # titlul de fereastra a display-ului
pygame.font.init()  # initializare font a jocului pt. a putea sa vedem (cifrele din patratele, scorul, etc...)

myfont = pygame.font.SysFont("Calibri", 30)  # nume font si marimea caracterelor
screen = pygame.display.set_mode((W, H))  # rezolutia jocului


def new_number(k=1):  # Marian, k = 1 pt. ca sa se afiseze un singur numar la fiecare mutare
    # np where(conditie) returneaza poz. elem. care respecta conditia
    # zip gupeaza linia cu coloana
    # list este un constructor si returneaza o lista
    free_poss = list(zip(*np.where(grid == 0)))
    # => free_pos = toate pozitiile grupate (l cu c) care nu au valori, pt. a putea pune numere
    for pos in random.sample(free_poss, k=k):  # random.sample(lista, x) returneaza x elemente random din lista
        if random.random() < .1:  # random.random() returneaza un numar intre [0.0, 1.0]
            grid[pos] = 4
        else:
            grid[pos] = 2


def _get_nums(array):  # Sergiu
    array_n = array[array != 0]  # salvam in lista, doar numerele != 0 pt. a face verificarea de valori mai usoara
    array_n_final = []
    skip = False

    for j in range(len(array_n)):
        if skip:
            skip = False
            continue
        if j != len(array_n) - 1 and array_n[j] == array_n[j + 1]:  # verificam vecinii
            new_n = array_n[j] * 2
            skip = True
        else:
            new_n = array_n[j]

        array_n_final.append(new_n)

    return np.array(array_n_final)  # returnam noua lista in urma mutarii


def make_move(move):  # Sergiu
    for i in range(N):
        if move in "lr":  # stanga/dreapta
            array = grid[i, :]  # lucram pe linii
        else:  # sus/jos
            array = grid[:, i]  # lucram pe coloane

        flipped = False
        if move in "rd":
            # dreapta/jos => intoarcem linia invers (ex.: 2 0 2 2 -> pt. st => 4 2 VS pt. dr => 2 4)
            flipped = True
            array = array[::-1]  # [::-1] -> intoarcem, adica de la sfarsit spre inceput

        array_n = _get_nums(array)
        new_array = np.zeros_like(array)  # np.zeros_like(dim) return un sir cu valori 0 de dimensiunea dim
        new_array[:len(array_n)] = array_n

        if flipped:
            new_array = new_array[::-1]  # daca a fost intoarsa, o intoarcem din nou ca sa fie ca la inceput

        if move in "lr":
            grid[i, :] = new_array  # salvam pe linii
        else:
            grid[:, i] = new_array  # salvam pe coloane


def draw_game():  # Marian
    screen.fill(CP["background"])  # culorile din background

    for i in range(N):
        for j in range(N):
            n = grid[i][j]

            rect_x = j * W // N + SPACING
            rect_y = i * H // N + SPACING
            rect_w = W // N - 2 * SPACING
            rect_h = H // N - 2 * SPACING

            # cu Rect accesam ce este in interiorul formelor pe care le desenam
            pygame.draw.rect(screen,
                             CP[n],
                             pygame.Rect(rect_x, rect_y, rect_w, rect_h),
                             border_radius=8)

            if n == 0:
                continue
            text_surface = myfont.render(str(n), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(rect_x + rect_w / 2, rect_y + rect_h / 2))
            screen.blit(text_surface, text_rect)  # blit = desenam


def wait_for_key():  # Marian
    while True:
        for event in pygame.event.get():  # verifica toate evenimentele din pygame
            if event.type == QUIT:  # X-ul din fereastra jocului
                end()
            if event.type == KEYDOWN:  # cand o tasta este apasata
                if event.key == K_UP:
                    return "u"
                elif event.key == K_RIGHT:
                    return "r"
                elif event.key == K_LEFT:
                    return "l"
                elif event.key == K_DOWN:
                    return "d"
                elif event.key == K_ESCAPE or event.key == K_q:  # o oprire fortata cu tasta q (de exemplu)
                    end()


def game_over():  # David
    global grid
    grid_bu = grid.copy()
    for move in 'lrud':
        make_move(move)
        # daca dupa o mutare, matricea veche deja difera de cea noua => nu mai trebuie sa verificam restul mutarilor
        if not all((grid == grid_bu).flatten()):  # flatten = matricea devine sir pt. a face compararile mai usor
            grid = grid_bu
            return False
    return True


def game_over_text():  # David
    screen.fill(CP["menu"])
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # daca apas pe X (Close) o sa inchida jocul
                end()
        text = myfont.render("Ai pierdut!", True, CP["textfinish"])
        textpos = text.get_rect()  # pt. ca suprafetele nu au o pozitie, trebuie stocate in blit
        textpos.center = (W // 2, H // 2)
        screen.blit(text, textpos)
        pygame.display.update()


def end():  # David
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def play():  # David
    new_number(k=2)  # initializam 2 pozitii random
    while True:
        draw_game()
        pygame.display.flip()  # updateaza continutul INTREGULUI display (altfel este blackscreen)
        cmd = wait_for_key()
        old_grid = grid.copy()  # facem o copie pt. a putea verifica, dupa mutare, diferentele new vs old grid
        make_move(cmd)
        print(grid)  # daca dorim sa observam mutarea tablei in consola
        if game_over():
            game_over_text()
        if not all((grid == old_grid).flatten()):  # cand matricea veche vs noua sunt diferite => sunt posibile mutari
            new_number()  # atunci la fiecare miscare, se genereaza un numar, 2 sau 4, pe o pozitie random


play()
