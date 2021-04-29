import numpy as np
import pygame

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