import numpy as np
import pygame
import random

N = 4  # 4 linii si 4 coloane
grid = np.zeros((N, N), dtype=int)  # initializam grila care este un patrat de N linii si coloane si toate valorile sunt de tip int
W = 400  # latime
H = W  # inaltime
SPACING = 10  # spatiul dintre patratele
pygame.init()
pygame.display.set_caption("2048")  # titlul jocului
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)  # formatul jocului si marimea caracterelor
screen = pygame.display.set_mode((W, H))


def new_number(k=1):
    free_poss = list(zip(*np.where(grid == 0)))  # zip le grupeaza 2 cate 2, adica inainte lista era [(0,0,0,0,1,1,etc...)], acum este [(0,0),(0,1),(0,2),(0,3),(1,0),etc...]
    for pos in random.sample(free_poss, k=k):  # cand incepi jocul ai valori pe 2 pozitii (acel k)
        if random.random() < .1:  # probablitatea sa fie 4 este de 10 %
            grid[pos] = 4
        else:
            grid[pos] = 2  # in restul cazurilor, 90% din acestea, valoarea este 2
