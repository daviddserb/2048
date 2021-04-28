import numpy as np
import random

N = 4

grid = np.zeros((N, N))  # un grid de N, N (pentru ca ii un patrat de N linii si N coloane, N fiind 4)

poss = list((zip(*np.where(grid == 0))))  # zip le grupeaza 2 cate 2, adica inainte lista ta era [(0, 0, 0, 0, 1, 1, etc...)] acum este [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), etc...]

for pos in random.sample(poss, k=2):  # cand incepi jocul, ai valori pe 2 pozitii (acel k)
    if random.random() < .1:
        grid[pos] = 4  # valoarea poate sa fie 4
    else:
        grid[pos] = 2  # dar poate sa fie si 2 (cea mai mare probabilitate)

print(grid)
