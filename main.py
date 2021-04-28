import numpy as np
import random

N = 4


class Py2048Logic:  # fac doar logica acum
    def __init__(self):
        self.grid = np.zeros((N, N))  # initializam grila de (N, N), pentru ca este un patrat de N linii si N coloane)

    def __str__(self):  # vrem sa pritam doar grila momentan...
        return str(self.grid)

    def new_number(self, k=1):
        free_poss = list((zip(*np.where(self.grid == 0))))  # zip le grupeaza 2 cate 2, adica inainte lista ta era [(0, 0, 0, 0, 1, 1, etc...)] acum este [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), etc...]

        for pos in random.sample(free_poss, k=k):  # cand incepi jocul, ai valori pe 2 pozitii (acel k)
            if random.random() < .1:  # aici cred ca a pus .1 pentru ca probablitatea sa fie 4 este mai mica de 10 %
                self.grid[pos] = 4  # valoarea poate sa fie 4
            else:
                self.grid[pos] = 2  # dar poate sa fie si 2 (cea mai mare probabilitate)


if __name__ == '__main__':  # initializam jocul
    game = Py2048Logic()
    print(game)
