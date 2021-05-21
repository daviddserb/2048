import numpy as np
import random
import pygame
import sys
from pygame.locals import *
from constants import CP

N = 4  # matrice patratica de 4 linii si 4 coloane
grid = np.zeros((N, N), dtype=int)  # face matrice cu valori de 0 si date de tip int, adica numere intregi
W = 400  # latime
H = W  # inaltime
SPACING = 10
pygame.init()  # initializam jocul
pygame.display.set_caption("2048")  # titlul jocului
pygame.font.init()  # initializare font
myfont = pygame.font.SysFont("Calibri", 30)  # formatul jocului si marimea caracterelor
screen = pygame.display.set_mode((W, H))  # rezolutia jocului


def new_number(k=1):  # Marian, k = 1 sa afiseze un numar random la fiecare mutare
    free_poss = list(zip(*np.where(grid == 0)))  # np.where returneaza pozitiile elementelor, zip grupeaza linie coloana
    for pos in random.sample(free_poss, k=k):  # random.sample(lista, k) iti returneaza k elemente random din lista ta
        if random.random() < .1:  # random.random() returneaza un numar intre 0 si 1
            grid[pos] = 4  # valoarea poate sa fie 4 (probabilitate de sub 10% [acel <.1])
        else:
            grid[pos] = 2  # dar poate sa fie si 2 (probabilitate mai mare - peste 90%)


def _get_nums(this):  # Sergiu
    this_n = this[this != 0]  # salvam in this_n, lista this cu valorile diferite de 0
    this_n_sum = []
    skip = False  # variabila de tip flag
    for j in range(len(this_n)):
        if skip:  # daca skip ii adevarat
            skip = False  # il reinitializam cu False
            continue  # sarim peste tot si reintram in for
        if j != len(this_n) - 1 and this_n[j] == this_n[j + 1]:  # verificam vecinii si ne oprim la penultima poz.
            new_n = this_n[j] * 2
            skip = True
        else:  # raman neschimbate
            new_n = this_n[j]
        this_n_sum.append(new_n)  # adaugam elementul new_n la inceputul listei this_n_sum
    return np.array(this_n_sum)  # returnezi lista ta noua in numpy


def make_move(move):  # Sergiu
    print(move)
    for i in range(N):
        if move in "lr":  # daca mutarea este stanga sau dreapta
            this = grid[i, :]  # lucram pe linii si luam cate un element in ordine
        else:  # "ud"
            this = grid[:, i]  # lucram pe coloane si luam cate un element in ordine
        flipped = False
        if move in "rd":  # pt. a reproduce miscarea de la "lu"
            flipped = True
            this = this[::-1]  # intoarcem matricea
        this_n = _get_nums(this)
        new_this = np.zeros_like(this)  # initializam lista new_this cu 0-uri de dimensiunea listei this
        new_this[:len(this_n)] = this_n  # aici incepe miscarea: punem valorile diferite de 0 spre directia care trebuie
        if flipped:
            new_this = new_this[::-1]  # o intoarcem din nou sa fie ca la inceput
        if move in "lr":
            grid[i, :] = new_this  # salvam liniile in liniile matricei
        else:
            grid[:, i] = new_this  # salvam coloanele in coloanele matricei


def draw_game():  # Marian
    screen.fill(CP["background"])  # culorile din background
    for i in range(N):  # parcurgem matricea
        for j in range(N):
            n = grid[i][j]
            rect_x = j * W // N + SPACING  # patratelele de pe linii si coloane
            rect_y = i * H // N + SPACING  # (ex.: 101 / 4 = 25 rest 1, 101 // 4 = 25) afiseaza valoarea intreaga
            rect_w = W // N - 2 * SPACING  # spatierea patretelor pe latime si inaltime
            rect_h = H // N - 2 * SPACING
            pygame.draw.rect(screen,  # functia: pygame.draw.rect(Surface, color, Rect, width)
                             CP[n],
                             pygame.Rect(rect_x, rect_y, rect_w, rect_h),
                             border_radius=8)  # rotunjirea coltului
            if n == 0:  # ca sa nu printam 0 pe pozitii
                continue  # si atunci sarim peste instructiunile de sub el, si intra in for-ul cu j
            text_surface = myfont.render(str(n), True, (0, 0, 0))  # punem valorile/cifrele prin f string
            text_rect = text_surface.get_rect(center=(rect_x + rect_w / 2,  # punerea cifrelor in mijlocul patratelelor
                                                      rect_y + rect_h / 2))
            screen.blit(text_surface, text_rect)  # screen.blit(text, pozitia)


def wait_for_key():  # Marian
    while True:
        for event in pygame.event.get():  # verifica toate evenimentele din pygame
            if event.type == QUIT:
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
                elif event.key == K_q or event.key == K_ESCAPE:  # o oprire fortata cu tasta q
                    end()


def game_over():  # David
    global grid
    grid_bu = grid.copy()  # pt. ca make_move schimba grila, facem o copie
    # daca dupa prima miscare, se schimba, nu mai trebuie sa le verificam si pe restul
    for move in 'lrud':  # daca se face o miscare random, dar care sa nu inchida jocul
        make_move(move)
        if not all((grid == grid_bu).flatten()):  # flatten = matricea o aranjeaza pe linie, facem compararile mai usor
            grid = grid_bu  # pentru ca se pot face miscari, atunci ne reintoarcem pe grila noastra precedenta
            return False  # jocul ii bun
    return True  # game over


def game_over_text():  # David
    screen.fill(CP["menu"])  # culori background la joc
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # daca apas pe X (Close)
                end()  # il inchide
        text = myfont.render("Ai pierdut!", True, CP["textfinish"])
        textpos = text.get_rect()  # pt. ca suprafetele nu au o pozitie, trebuie stocate in blit.
        textpos.center = (W // 2, H // 2)
        screen.blit(text, textpos)  # afisam textul pe ecran "Ai pierdut"
        pygame.display.update()  # daca ai terminat jocul, trebuie sa apara o noua poza pe ecran cu textul "Ai pierdut"


def end():  # David
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def play():  # David
    new_number(k=2)  # initializam cele 2 pozitii cu valori (inceputul jocului)
    while True:  # o structura repetitiva in care nu vrem si linia 139
        draw_game()  # desenam jocul cu patratele cu tot
        pygame.display.flip()  # updateaza continutul intregului display (altfel ii blackscreen)
        cmd = wait_for_key()  # dam o comanda de la tastatura
        old_grid = grid.copy()  # facem copie intregii grilei pt. a nu o pierde dupa ce se fac calculele
        make_move(cmd)  # incepem prelucrarea instructiunilor din functia make_move cu comanda noastra
        print(grid)  # printam grida (daca dorim)
        if game_over():  # daca in functia game_over avem return True, atunci ai pierdut
            game_over_text()
        if not all((grid == old_grid).flatten()):  # daca mai putem misca matricea intr-o directie
            new_number()  # atunci la fiecare miscare, se genereaza un numar, 2 sau 4, pe o pozitie random


play()
