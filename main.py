import numpy as np
import pygame
import random

N = 4
grid = np.zeros((N, N), dtype=int)  # initializam grila de (N, N), pentru ca este un patrat de N linii si N coloane si variabilele de timp int
W = 400  # latime
H = W  # inaltime
SPACING = 10
pygame.init()
pygame.display.set_caption("2048")  # titlul jocului
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)  # formatul jocului si marimea caracterelor
screen = pygame.display.set_mode((W, H))

def new_number(k=1):
    free_poss = list(zip(*np.where(grid == 0))) #zip le grupeaza 2 cate 2, adica inainte lista era [(0,0,0,0,1,1,etc...)], acum este [(0,0),(0,1),(0,2),(0,3),(1,0),etc...]
    for pos in random.sample(free_poss, k=k): #cand incepi jocul ai valori pe 2 pozitii (acel k)
        if random.random() < .1: #pentru a fi 4 trebuie ca valoarea sa fie sub 10%
            grid[pos] = 4 #valoarea poate sa fie 4 (probabilitate de sub 10% [acel <.1])
        else:
            grid[pos] = 2 #dar poate sa fie si 2 (probabilitate mai mare - peste 90%)