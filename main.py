import numpy as np

N = 4

grid = np.zeros((N, N))  # o grila de (N, N), pentru ca este un patrat de N linii si N coloane

poss = list((zip(*np.where(grid == 0))))  # zip le grupeaza 2 cate 2, adica inainte lista era [(0, 0, 0, 0, 1, 1, etc...)] acum este [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), etc...]

print(grid)
print(poss)
